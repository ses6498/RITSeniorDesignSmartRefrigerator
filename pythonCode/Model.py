'''
Created on Mar 13, 2012

@author: Steven
'''
import threading
import datetime

import Inventory
import HourlyTasks
import TimeWrapper
import ExpirationDatePrediction

import sqlalchemy
import sqlalchemy.orm

class UpcLutItem (object):
    
    def __init__(self, upc, description, gs1Category):
        self.upc = upc
        self.description = description
        self.gs1Category = gs1Category
        
    def __repr__(self):
        return '<UpcLutItem(%d, %s, %s)>' % (self.upc, self.description, self.gs1Category)
    
class Model (threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, controller):
        '''
        Constructor
        '''
        self.viewObj = None
        self.controllerObj = controller
        
        self.hourlyTasks = HourlyTasks.HourlyTasks(self)
        
        threading.Thread.__init__(self)
#        self.start()
        
        self.databaseConnectionInitialization()
        self.initializeUPCLUT()
        self.initializeExpirationWarningLUT()
        self.currentInventory = Inventory.Inventory(self)
        self.timeWrapper = TimeWrapper.TimeWrapper()
        self.expirationDatePredictor = ExpirationDatePrediction.ExpirationDatePrediction(self)
        
        self.currentItem = None
        
        self.mode = self.controllerObj.CHECK_IN_MODE
        
    def echoTime (self):
        print self.timeWrapper.returnTime()
        
    def databaseConnectionInitialization (self):
#        engine = sqlalchemy.create_engine('mysql://ses6498:seNi{}R1)esign@localhost/smartrefrigeratorDb')
        self.engine = sqlalchemy.create_engine('mysql://ses6498:seNi{}R1)esign@smartfridge.student.rit.edu/smartRefrigeratorDb')
        self.metadata = sqlalchemy.MetaData()        
        
    def initializeUPCLUT (self):
        upcLut = sqlalchemy.Table ('upcLut', self.metadata, \
                sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), \
                sqlalchemy.Column('upc', sqlalchemy.BigInteger), \
                sqlalchemy.Column('description', sqlalchemy.String(128)), \
                sqlalchemy.Column('gs1Category', sqlalchemy.String(8)))
        
        self.metadata.create_all (self.engine)
        sqlalchemy.orm.mapper(UpcLutItem, upcLut)
        
        Session = sqlalchemy.orm.sessionmaker(bind=self.engine)
        self.session = Session()
        
        # This will really be read from config file
        flatfile = []
        flatfile.append([36600814815, 'Chap Stick', 'GS1Cde01'])
        flatfile.append([38000299377, 'Pop Tart - Apple', 'GS1Cde02'])
        flatfile.append([38000318405, 'Pop Tart- Cherry', 'GS1Cde01'])
        
        for item in flatfile:
            if self.session.query(UpcLutItem).filter(UpcLutItem.upc==item[0]).count() == 0:
                upcLutItem = UpcLutItem(item[0], item[1], item[2])
                self.session.add(upcLutItem)
                
        self.session.commit()
    
    def upcLookup (self, upc):
        return self.session.query(UpcLutItem).filter(UpcLutItem.upc==upc).count() > 0
    
    def initializeExpirationWarningLUT (self):
        self.expirationWarningLUT = dict()
    
    def expirationDateLookup (self, gs1Catagory):
        found = gs1Catagory in self.gs1LUT
        return found
    
    def advanceHour (self):
        self.hourlyTasks.trigger()
        self.timeWrapper.advanceHour()
    
    def addItem (self, upc, params=None):
        if params:
            print 'Not supported yet'
        else:
            upcInfo = self.session.query(UpcLutItem).filter(UpcLutItem.upc==upc).all()
            if len(upcInfo) != 1:
                print "THIS IS AN ERROR CASE"
            upcInfo = upcInfo[0]
            
            expDate = 'Unknown'
            expData = self.expirationDatePredictor.expirationDateLookup(upcInfo.gs1Category)
            if expData:
                expDate = self.timeWrapper.returnTime()
                expDate = expDate + datetime.timedelta(days=expData[0].expirationEstimate)
            
            purDate = self.timeWrapper.returnTime()
            item = Inventory.InventoryItem(upc=long(upc), upcString=upc, description=upcInfo.description, purchaseDate=purDate, \
                                               expirationDate=expDate)
            self.hourlyTasks.registerItemTask(purDate.hour, upc)
            
            self.currentItem = item
            self.controllerObj.setLastItem(self.mode)
            self.controllerObj.updateItemInfo(item)
            
            duplicate = self.currentInventory.returnItem(upc) != []
            
            if not duplicate:
                self.controllerObj.addInventoryItem(item)
            else:
                self.controllerObj.addDuplicateInventoryItem(item, \
                    len(self.currentInventory.returnItem(upc))+1)
                
            self.currentInventory.addItem(item)
            self.checkItemExpiration([upc])
            
    def recallItem (self, upc):
        if self.currentInventory.searchItem(upc):
            info = self.currentInventory.returnItem(upc, sorted='purchase')
                
            if len(info) > 1:
                    self.controllerObj.duplicatePrompt(info)
            else:
                self.controllerObj.updateItemInfo(info[0])
                self.currentItem = info[0]
                self.controllerObj.setLastItem(self.mode)
                
            return True
        else:
            return False
            
    def recallDuplicateSelected (self, item):
        self.controllerObj.updateItemInfo(item)
        self.currentItem = item
        self.controllerObj.setLastItem(self.mode)
            
    def genericRemoveTasks (self):
        if self.currentItem:
            
            numDuplicates = len(self.currentInventory.returnItem(self.currentItem.upc))
            
            if numDuplicates > 1:
                self.controllerObj.removeDuplicateInventoryItem(self.currentItem, numDuplicates-1)
            else:
                self.controllerObj.removeInventoryItem(self.currentItem)
            
            self.currentInventory.removeItem(self.currentItem)
#            self.hourlyTasks.removeItemTask(self.currentItem)
                
#            if self.currentItem in self.expirationWarningLUT:
#                del self.expirationWarningLUT[self.currentItem]
#                self.controllerObj.removeExpirationWarning(self.currentItem)
            
    def expiredItem (self):
#        self.expirationDatePredictor.earlyExpiration(self.currentItem, expirationDate)
        self.genericRemoveTasks()
        
    def consumedItem (self):
        self.genericRemoveTasks()
            
    def removeLastItem (self):
        if self.currentItem:
            self.genericRemoveTasks()
            self.currentItem = None
            self.controllerObj.clearLastItem()
            
    def upcEntered (self, upc, params=None):
        if self.mode == self.controllerObj.CHECK_IN_MODE:
            if self.upcLookup(upc):
                self.addItem(upc, params)
                return self.controllerObj.VALID_ITEM
            else:
                return self.controllerObj.UNKNOWN_ITEM
        elif self.mode ==self.controllerObj.CHECK_OUT_MODE:
            if self.upcLookup(upc):
                if self.recallItem(upc):
                    return self.controllerObj.VALID_ITEM
                else:
                    return self.controllerObj.MISSING_ITEM
            else:
                return self.controllerObj.UNKNOWN_ITEM
        
    def checkInMode (self):
        self.mode = self.controllerObj.CHECK_IN_MODE
        return self.currentItem
        
    def checkOutMode (self):
        self.mode = self.controllerObj.CHECK_OUT_MODE
        return self.currentItem
    
    def checkItemExpiration (self, upcs):
        time = self.timeWrapper.returnTime()
        
        for upc in upcs:
            if self.currentInventory.searchItem(upc):
                info = self.currentInventory.returnItem(upc)
                
                # THIS IS A HACK TODO TODO TODO FIX ME
                info = info[0]
                delta = info.expirationDate - time
                update = upc in self.expirationWarningLUT
                
                if delta.days < 5:
                    if update:
                        if self.expirationWarningLUT[upc] != delta.days:
                            self.expirationWarningLUT[upc] = delta.days
                            self.controllerObj.expirationWarning(upc, delta.days, update)
                    else:
                        self.controllerObj.expirationWarning(upc, delta.days, update)
                        self.expirationWarningLUT[upc] = delta.days
        
    def clearInventory (self):
        self.currentInventory.clear()
        
    def run(self):
        a = 5
#        print "hi this is the model thread"