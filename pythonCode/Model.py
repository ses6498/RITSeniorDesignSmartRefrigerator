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
        self.start()
        
        self.currentInventory = Inventory.Inventory(self)
        self.timeWrapper = TimeWrapper.TimeWrapper()
        
        self.initializeUPCLUT()
        self.initializeExpirationWarningLUT()
        
        self.expirationDatePredictor = ExpirationDatePrediction.ExpirationDatePrediction()
        
        self.currentItem = None
        
        self.mode = self.controllerObj.CHECK_IN_MODE
        
    def echoTime (self):
        print self.timeWrapper.returnTime()
        
    def initializeUPCLUT (self):
        self.upcLUT = dict()
        self.upcLUT['036600814815'] = ('Chap Stick', 'GS1 Code 1')
        self.upcLUT['038000299377'] = ('Pop Tart - Apple', 'GS1 Code 2')
        self.upcLUT['038000318405'] = ('Pop Tart - Cherry', 'GS1 Code 1')
    
    def upcLookup (self, upc):
        found = upc in self.upcLUT
        return found
    
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
            upcInfo = self.upcLUT[upc]
            
            expDate = 'Unknown'
            expData = self.expirationDatePredictor.expirationDateLookup(upcInfo[1])
            if expData[0]:
                expDate = self.timeWrapper.returnTime()
                expDate = expDate + datetime.timedelta(days=expData[1])
            
            purDate = self.timeWrapper.returnTime()
            item = Inventory.InventoryItem(upc=long(upc), upcString=upc, name=upcInfo[0], purchaseDate=purDate, \
                                               expirationDate=expDate)
#            itemInfo['name'] = upcInfo[0]
#            itemInfo['upc'] = upc
#            itemInfo['purchaseDate'] = purDate
#            itemInfo['expirationDate'] = expDate
            self.hourlyTasks.registerItemTask(purDate.hour, upc)
            
            self.currentItem = upc
            self.controllerObj.setLastItem(self.mode)
            
            self.controllerObj.updateItemInfo(item)
            item.identifier = self.controllerObj.inventoryAddition(item)
            self.currentInventory.addItem(item)
            
            self.checkItemExpiration([upc])
            
    def recallItem (self, upc, params=None):
        if params:
            print 'Not supported yet'
        else:
            if self.currentInventory.searchItem(upc):
                info = self.currentInventory.returnItem(upc)
                self.controllerObj.updateItemInfo(info)
                self.currentItem = upc
                self.controllerObj.setLastItem(self.mode)
                return True
            else:
                return False
            
    def genericRemoveTasks (self):
        if self.currentItem:
            deletedItems = self.currentInventory.removeItem(self.currentItem)
            
            for item in deletedItems:
                self.controllerObj.inventoryDeletion(item.upcString, item.identifier)
                self.hourlyTasks.removeItemTask(item.purchaseDate.hour, item.upcString)
                
                if self.currentItem in self.expirationWarningLUT:
                    del self.expirationWarningLUT[self.currentItem]
                    self.controllerObj.removeExpirationWarning(self.currentItem)
            
    def expiredItem (self):
        print self.currentInventory.returnItem(self.currentItem)
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
                if self.recallItem(upc, params):
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