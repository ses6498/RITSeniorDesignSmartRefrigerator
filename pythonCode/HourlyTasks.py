'''
Created on Mar 20, 2012

@author: Steven
'''
import threading

class HourlyTasks (threading.Thread):
    '''
    classdocs
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        self.lock = threading.Event()
        self.synch = threading.Event()
        self.running = True
        
        self.model = model
        
        threading.Thread.__init__(self)
        self.start()
        
    def run (self):
        while self.running:
            self.lock.wait(10.0)
            
            if self.running:
                self.model.checkItemExpiration()
                self.lock.clear()
                self.synch.set()
            
    def trigger (self):
        self.lock.set()
        self.synch.wait()
        self.synch.clear()
        
    def terminate (self):
        self.running = False
        self.lock.set()