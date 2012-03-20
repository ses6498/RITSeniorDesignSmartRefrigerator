'''
Created on Mar 20, 2012

@author: Steven
'''
import datetime

class TimeWrapper (object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.offset = 0
        
    def advanceHour (self, offset):
        self.offset = self.offset + offset
        
    def returnTime (self):
        return datetime.datetime.now() + datetime.timedelta(hours=self.offset)
        
        