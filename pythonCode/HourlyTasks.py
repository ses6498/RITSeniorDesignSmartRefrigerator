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
        self.running = True
        
        self.model = model
        
        threading.Thread.__init__(self)
        self.start()
        
    def run (self):
        while self.running:
            self.lock.wait(10.0)
            self.model.echoTime ()
            self.lock.clear()
       
    def trigger (self):
        self.lock.set()
        
        