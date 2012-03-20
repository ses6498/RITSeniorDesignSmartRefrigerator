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
        
        self.expHourChecks = [[] for x in range(24)]
        
        threading.Thread.__init__(self)
        self.start()
        
    def run (self):
        while self.running:
            self.lock.wait(10.0)
            self.model.echoTime ()
            self.checkExpiration()
            self.lock.clear()
            self.synch.set()
            
    def checkExpiration (self):
        time = self.model.timeWrapper.returnTime()
        self.model.checkItemExpiration(self.expHourChecks[time.hour])
       
    def trigger (self):
        self.lock.set()
        self.synch.wait()
        self.synch.clear()
        
    def registerItemTask (self, hour, upc):
        self.expHourChecks[hour].append(upc)
        
    def removeItemTask (self, hour, upc):
        self.expHourChecks[hour].remove(upc)