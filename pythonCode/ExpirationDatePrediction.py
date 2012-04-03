'''
Created on Mar 25, 2012

@author: Steven
'''
import sqlalchemy
import sqlalchemy.orm
import numpy

import Model
import Inventory

class Gs1LutItem (object):
    
    def __init__(self, gs1Category, expirationEstimate):
        self.gs1Category = gs1Category
        self.expirationEstimate = expirationEstimate
        
    def __repr__(self):
        return '<Gs1LutItem(%s, %s)>' % (self.gs1Category, self.expirationEstimate)

class ExpirationDatePrediction (object):
    '''
    classdocs
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        
        self.initializeGS1LUT()
        
    def initializeGS1LUT (self):
        gs1Lut = sqlalchemy.Table ('gs1Lut', self.model.metadata, \
                sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                sqlalchemy.Column('gs1Category', sqlalchemy.String(13), primary_key=True), \
                sqlalchemy.Column('expirationEstimate', sqlalchemy.Float))
        
        self.model.metadata.create_all (self.model.engine)
        sqlalchemy.orm.mapper (Gs1LutItem, gs1Lut)
        
        Session = sqlalchemy.orm.sessionmaker(bind=self.model.engine)
        self.session = Session()
        
        # This will really be read from config file
        
    def populateGs1Lut (self):
        flatfile = []
        flatfile.append(['GS1Cde01', 5.0])
        flatfile.append(['GS1Cde02', 3.0])
        
        items = self.session.query(Gs1LutItem).all()
        for item in items:
            self.session.delete(item)
        self.session.commit()
        
        for item in flatfile:
            if self.session.query(Gs1LutItem).filter(Gs1LutItem.gs1Category==item[0]).count() == 0:
                gs1LutItem = Gs1LutItem(item[0], item[1])
                self.session.add(gs1LutItem)
        self.session.commit()
        
    def expirationDateLookup (self, gs1Category):
        returnValue = self.session.query(Gs1LutItem).filter(Gs1LutItem.gs1Category==gs1Category).all()
        
        if not returnValue:
            print "ERROR GS1 MISSING"
        elif len(returnValue) > 1:
            print "DUP GS1 ERROR"
            
        return numpy.round(returnValue[0].expirationEstimate)
    
    def adjustExpirationEstimate (self, item):
        time = self.model.timeWrapper.returnTime()
        secondsPerDay = 86400.0
        
        upcLutItem = self.session.query(Model.UpcLutItem).filter(Model.UpcLutItem.upc==item.upc).all()
        if len(upcLutItem) != 1 : print 'Error Condition'
        upcLutItem = upcLutItem[0]
        oldGs1LutItem = self.session.query(Gs1LutItem).filter(Gs1LutItem.gs1Category==upcLutItem.gs1Category).all()
        if len(oldGs1LutItem) != 1 : print 'Error Condition'
        oldGs1LutItem = oldGs1LutItem[0]
    
        # N4 Exponential Moving Averager
        newExpEstimate = time - item.purchaseDate
        newExpEstimate = newExpEstimate.total_seconds() / secondsPerDay
        newExpEstimate = 0.5 * oldGs1LutItem.expirationEstimate + 0.5 * newExpEstimate
            
        gs1LutItem = self.session.query(Gs1LutItem).filter(Gs1LutItem.gs1Category=='C' + str(item.upc)).all()
            
        # Check if it has a custom or not first
        if gs1LutItem:
            if len(gs1LutItem) != 1 : print 'Error Condition'
            gs1LutItem = gs1LutItem [0]
            gs1LutItem.expirationEstimate = newExpEstimate
        # Add new custom item
        else:
            upcLutItem.gs1Category = 'C' + str(item.upc)
            gs1LutItem = Gs1LutItem ('C'+str(item.upc), newExpEstimate)
            self.session.add(gs1LutItem)
        
        self.session.commit()
        
    def earlyExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate
        
    def lateExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate