'''
Created on Mar 25, 2012

@author: Steven
'''
import sqlalchemy
import sqlalchemy.orm

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
                sqlalchemy.Column('gs1Category', sqlalchemy.String(8), primary_key=True), \
                sqlalchemy.Column('expirationEstimate', sqlalchemy.Integer))
        
        self.model.metadata.create_all (self.model.engine)
        sqlalchemy.orm.mapper (Gs1LutItem, gs1Lut)
        
        Session = sqlalchemy.orm.sessionmaker(bind=self.model.engine)
        self.session = Session()
        
        # This will really be read from config file
        
    def populateGs1Lut (self):
        flatfile = []
        flatfile.append(['GS1Cde01', 5])
        flatfile.append(['GS1Cde02', 3])
        
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
            
        return returnValue
        
    def earlyExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate
        
    def lateExpiration (self, purchaseDate, expirationDate):
        print purchaseDate
        print expirationDate