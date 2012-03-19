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
    
    def size (self):
        return len(self.currentInventory)