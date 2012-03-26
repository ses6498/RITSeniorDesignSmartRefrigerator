'''
Created on Mar 25, 2012

@author: Steven
'''

class ExpirationDatePrediction (object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.initializeGS1LUT()
        
    def initializeGS1LUT (self):
        self.gs1LUT = dict()
        self.gs1LUT['GS1 Code 1'] = 5
        self.gs1LUT['GS1 Code 2'] = 3
        
    def expirationDateLookup (self, gs1Catagory):
        if gs1Catagory in self.gs1LUT:
            return (True, self.gs1LUT[gs1Catagory])
        else:
            return (False, None)
        
    def earlyExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate
        
    def lateExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate