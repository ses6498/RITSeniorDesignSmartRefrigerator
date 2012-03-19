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
        self.modelObj = Model.Model(self)
        self.viewObj = View.View(self)
        
        self.viewObj.mainLoop()
        
    def upcEntered (self, upc, valid=True):
        # Check with Model
        if valid:
            if self.modelObj.upcLookup(upc):
                self.viewObj.knownUPC(upc)
                self.modelObj.addItem(upc)
            else:
                self.viewObj.unknownUPC(upc)
        else:
            self.viewObj.invalidUPC(upc)
            
    def updateItemInfo (self, info):
        self.viewObj.showItemInfo(info)
            
    def inventoryAddition (self, item):
        self.viewObj.addInventoryItem(item)
        
if __name__ == '__main__':
    
    controllerObj = Controller()