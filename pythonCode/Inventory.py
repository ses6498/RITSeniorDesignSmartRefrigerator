'''
Created on Mar 18, 2012

@author: Steven
'''

class Inventory ():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.currentInventory = dict()
        
    def addItem (self, item, info):
        self.currentInventory[item] = info
        
    def returnItem (self, item):
        return self.currentInventory[item]
        
    def removeItem (self, item):
        returnValue = self.currentInventory[item]
        del self.currentInventory[item]
        
        return returnValue
    
    def addIdentifier (self, item, identifier):
        if item[0] in self.currentInventory:
            info = self.currentInventory[item[0]]
            info = info + (identifier,)
            self.currentInventory[item[0]] = info
    
    def searchItem (self, item):
        return item in self.currentInventory
    
    def clear (self):
        self.currentInventory.clear()
    
    def size (self):
        return len(self.currentInventory)
    