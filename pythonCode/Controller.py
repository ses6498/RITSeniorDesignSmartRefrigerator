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
        
        self.viewObj = View.View(self)
        self.modelObj = Model.Model(self)
        
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
            
    def itemExpired (self, identifier=None):
        self.modelObj.expiredItem(identifier)
        
    def itemConsumed (self, identifier=None):
        self.modelObj.consumedItem(identifier)
        
    def addExpirationWarning (self, item, severity):
        self.viewObj.addExpirationWarning(item, severity)
        
    def updateExpirationWarning (self, item, severity):
        self.viewObj.updateExpirationWarning(item, severity)
        
    def removeExpirationWarning (self, item):
        self.viewObj.removeExpirationWarning(item)
        
    def clearExpirationWarnings (self):
        self.viewObj.clearExpirationWarnings()
        
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
            
    def updateItemInfo (self, item):
        self.viewObj.showItemInfo(item)
            
    def addInventoryItem (self, item):
        self.viewObj.addInventoryItem(item)
        
    def removeInventoryItem (self, item):
        self.viewObj.removeInventoryItem(item)
    
    def removeDuplicateInventoryItem (self, item, quantity):
        self.viewObj.removeDuplicateInventoryItem(item, quantity)
    
    def addDuplicateInventoryItem (self, item, quantity):
        self.viewObj.addDuplicateInventoryItem(item, quantity)
        
    def duplicatePrompt (self, items):
        self.viewObj.duplicatePrompt(items)
        
    def duplicateSelected (self, item):
        self.modelObj.recallDuplicateSelected(item)
        
    def createShoppingList (self, name):
        self.modelObj.addNewShoppingList(name)
        
    def createSuggestedShoppingList (self):
        self.modelObj.addNewSuggestedShoppingList()
        
    def createShoppingListItem (self, listIdentifier, itemIdentifier):
        self.modelObj.addNewShoppingListItem (listIdentifier, itemIdentifier)
        
    def createCustomShoppingListItem (self, listIdentifier, description, quantity):
        self.modelObj.addNewCustomShoppingListItem (listIdentifier, description, quantity)
    
    def addNewShoppingList (self, shoppingList):
        self.viewObj.addNewShoppingList(shoppingList)
        
    def addNewShoppingListItem (self, linker):
        self.viewObj.addNewShoppingListItem(linker)
        
    def updateShoppingListItem (self, linker):
        self.viewObj.updateShoppingListItem(linker)
        
    def updateShoppingListItemHandler (self, identifier, description, quantity):
        self.modelObj.updateShoppingListItem (identifier, description, quantity)
        
    def removeShoppingListHandler (self, identifier):
        self.modelObj.removeShoppingList (identifier)
        
    def removeShoppingListItemHandler (self, identifier):
        self.modelObj.removeShoppingListItem (identifier)
        
    def removeShoppingList (self, shoppingList):
        self.viewObj.removeShoppingList(shoppingList)
        
    def removeShoppingListItem (self, shoppingListItem):
        self.viewObj.removeShoppingListItem(shoppingListItem)
        
    def returnItemInfo (self, identifier):
        return self.modelObj.returnItemInfo (identifier)
    
    def clearInventory (self):
        self.modelObj.clearInventory()
        self.viewObj.clearInventory()
        
    def clearHistory (self):
        self.modelObj.clearHistory()
        
    def populateUpcLut (self):
        self.modelObj.populateUpcLut()
        
    def populateGs1Lut (self):
        self.modelObj.populateGs1Lut()
        
    def updateTemperature (self, temperature):
        self.viewObj.updateTemperature(temperature)
        
    def updateHumidity (self, humidity):
        self.viewObj.updateHumidity(humidity)
        
    def terminate (self):
        self.modelObj.terminate()
        
if __name__ == '__main__':
    
    controllerObj = Controller()