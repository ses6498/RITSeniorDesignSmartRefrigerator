'''
Created on Mar 13, 2012

@author: Steven
'''
import View
import Model

class Controller ():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.VALID_ITEM = 0
        self.UNKNOWN_ITEM = 1
        self.MISSING_ITEM = 2
        self.INVALID_UPC = 3
        
        self.CHECK_IN_MODE = 0
        self.CHECK_OUT_MODE = 1
        
        self.modelObj = Model.Model(self)
        self.viewObj = View.View(self)
        
        self.viewObj.mainLoop()
        
    def advanceHour (self):
        self.modelObj.advanceHour()
        
    def upcEntered (self, upc, valid=True):
        # Check with Model
        if valid:
            returnCode = self.modelObj.upcEntered(upc)
            
            if returnCode == self.VALID_ITEM:
                self.viewObj.knownUPC(upc)
            elif returnCode == self.UNKNOWN_ITEM:
                self.viewObj.unknownUPC(upc)
            elif returnCode == self.MISSING_ITEM:
                self.viewObj.missingUPC(upc)
        else:
            self.viewObj.invalidUPC(upc)
            
    def itemExpired (self):
        self.modelObj.expiredItem()
        
    def itemConsumed (self):
        self.modelObj.consumedItem()
        
    def removeLastItem (self):
        self.modelObj.removeLastItem()
        
    def clearLastItem (self):
        self.viewObj.clearLastItem()
        
    def setLastItem (self, state):
        self.viewObj.setLastItem(state)
            
    def checkInMode (self):
        state = self.modelObj.checkInMode()
        return state
        
    def checkOutMode (self):
        state = self.modelObj.checkOutMode()
        return state
            
    def updateItemInfo (self, info):
        self.viewObj.showItemInfo(info)
            
    def inventoryAddition (self, item):
        identifier = self.viewObj.addInventoryItem(item)
        self.modelObj.registerItemId (item, identifier)
        
    def inventoryDeletion (self, item, identifier):
        self.viewObj.removeInventoryItem(item, identifier)
        
    def clearInventory (self):
        self.modelObj.clearInventory()
        self.viewObj.clearInventory()
        
if __name__ == '__main__':
    
    controllerObj = Controller()