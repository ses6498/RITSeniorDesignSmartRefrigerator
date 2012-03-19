'''
Created on Mar 13, 2012

@author: Steven
'''
import threading
import time

import Inventory

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
        
        threading.Thread.__init__(self)
        self.start()
        
        self.currentInventory = Inventory.Inventory()
        
        self.initializeUPCLUT()
        
    def initializeUPCLUT (self):
        self.upcLUT = dict()
        self.upcLUT['036600814815'] = ('Chap Stick', 'GS1 Code')
    
    def upcLookup (self, upc):
        if upc in self.upcLUT:
            found = True
        else:
            found = False
            
        return found
    
    def addItem (self, upc, params=None):
        if params:
            print "Not supported yet"
        else:
            upcInfo = self.upcLUT[upc]
            itemInfo = (upcInfo[0], time.localtime(), time.localtime())
            self.currentInventory.addItem(upc, itemInfo)
            
            self.controllerObj.updateItemInfo(itemInfo)
            self.controllerObj.inventoryAddition((upc, itemInfo, self.currentInventory.size()))
        
    def run(self):
        
        print "hi this is the model thread"