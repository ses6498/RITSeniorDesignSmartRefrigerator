'''
Created on Mar 13, 2012

@author: Steven
'''
import threading
import datetime

import Inventory
import HourlyTasks
import TimeWrapper

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
        
        self.currentInventory = Inventory.Inventory()
        self.timeWrapper = TimeWrapper.TimeWrapper()
        
        self.initializeUPCLUT()
        self.initializeGS1LUT()
        
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
    
    def initializeGS1LUT (self):
        self.gs1LUT = dict()
        self.gs1LUT['GS1 Code 1'] = 5
        self.gs1LUT['GS1 Code 2'] = 3
    
    def expirationDateLookup (self, gs1Catagory):
        found = gs1Catagory in self.gs1LUT
        return found
    
    def advanceHour (self):
        self.timeWrapper.advanceHour()
        self.hourlyTasks.trigger()
    
    def addItem (self, upc, params=None):
        if params:
            print 'Not supported yet'
        else:
            upcInfo = self.upcLUT[upc]
            
            expDate = 'Unknown'
            if self.expirationDateLookup(upcInfo[1]):
                expDate = self.timeWrapper.returnTime()
                expDate = expDate + datetime.timedelta(days=self.gs1LUT[upcInfo[1]])
            
            purDate = self.timeWrapper.returnTime()
            itemInfo = (upcInfo[0], purDate, expDate)
            self.currentInventory.addItem(upc, itemInfo)
            self.hourlyTasks.registerItemTask(purDate.hour, upc)
            
            self.currentItem = upc
            self.controllerObj.setLastItem(self.mode)
            
            self.controllerObj.updateItemInfo(itemInfo)
            self.controllerObj.inventoryAddition((upc, itemInfo))
            
    def registerItemId (self, item, identifier):
        self.currentInventory.addIdentifier(item, identifier)
        
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
            
    def expiredItem (self):
        if self.currentItem:
            identifier = self.currentInventory.removeItem(self.currentItem)
            self.controllerObj.inventoryDeletion(self.currentItem, identifier[-1])
            self.hourlyTasks.removeItemTask(identifier[1].hour, self.currentItem)
        
    def consumedItem (self):
        if self.currentItem:
            identifier = self.currentInventory.removeItem(self.currentItem)
            self.controllerObj.inventoryDeletion(self.currentItem, identifier[-1])
            self.hourlyTasks.removeItemTask(identifier[1].hour, self.currentItem)
            
    def removeLastItem (self):
        if self.currentItem:
            identifier = self.currentInventory.removeItem(self.currentItem)
            self.controllerObj.inventoryDeletion(self.currentItem, identifier[-1])
            self.hourlyTasks.removeItemTask(identifier[1].hour, self.currentItem)
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
            info = self.currentInventory.returnItem(upc)
            delta = info[2] - time
            
            if delta.days < 1:
                print "RED"
            elif delta.days < 2:
                print "ORANGE"
            elif delta.days < 3:
                print "YELLOW"
            elif delta.days < 5:
                print "GREEN"
        
    def clearInventory (self):
        self.currentInventory.clear()
        
    def run(self):
        print "hi this is the model thread"