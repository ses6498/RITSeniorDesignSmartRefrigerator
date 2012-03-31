'''
Created on Mar 18, 2012

@author: Steven
'''
import sqlalchemy
import sqlalchemy.orm

class InventoryItem (object):
    
    def __init__(self, upc, upcString, description, purchaseDate, expirationDate):
        self.upc = upc
        self.upcString = upcString
        self.description = description
        self.purchaseDate = purchaseDate
        self.expirationDate = expirationDate
        self.identifier = None
        
    def __repr__(self):
        return "<Item('%d', '%s')>" % (self.upc, self.description)
    
class PurchaseHistoryItem (object):
    
    def __init__(self, upc, purchaseDate, quantity):
        self.upc = upc
        self.purchaseDate = purchaseDate
        self.quantity = quantity
    
    def __repr__(self):
        return "<HistoryItem('%d', '%s')>" % (self.upc, self.purchaseDate)

class Inventory ():
    '''
    classdocs
    '''
    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
                
        inventoryTable = sqlalchemy.Table('inventory', self.model.metadata, \
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), \
            sqlalchemy.Column('upc', sqlalchemy.BigInteger, primary_key=True), \
            sqlalchemy.Column('upcString', sqlalchemy.String(12)), \
            sqlalchemy.Column('description', sqlalchemy.String(128)), \
            sqlalchemy.Column('purchaseDate', sqlalchemy.DateTime), \
            sqlalchemy.Column('expirationDate', sqlalchemy.DateTime), \
            sqlalchemy.Column('identifier', sqlalchemy.String(28)))
        
        purchaseHistoryTable = sqlalchemy.Table('purchaseHistory', self.model.metadata, \
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), \
            sqlalchemy.Column('upc', sqlalchemy.BigInteger, primary_key=True), \
            sqlalchemy.Column('purchaseDate', sqlalchemy.DateTime), \
            sqlalchemy.Column('quantity', sqlalchemy.Integer))
        
        self.model.metadata.create_all (self.model.engine)
        sqlalchemy.orm.mapper(InventoryItem, inventoryTable)
        sqlalchemy.orm.mapper(PurchaseHistoryItem, purchaseHistoryTable)
        
        Session = sqlalchemy.orm.sessionmaker(bind=self.model.engine)
        self.session = Session()
        
        # Initial Inventory Addition
        for upc in self.session.query(InventoryItem.upc).distinct():
            lcv = 0
            
            for item in self.session.query(InventoryItem).filter(InventoryItem.upc==upc[0])\
                .order_by(InventoryItem.purchaseDate).all():
                if lcv == 0:
                    self.model.controllerObj.addInventoryItem(item)
                else:
                    self.model.controllerObj.addDuplicateInventoryItem(item, lcv+1)
                
                lcv += 1
        self.session.commit()        
        
    def addItem (self, item):
        self.session.add(item)
        
        purchaseHistoryItem = PurchaseHistoryItem (item.upc, item.purchaseDate, 1)
        self.session.add(purchaseHistoryItem)
        
        self.session.commit()
        
    def returnItem (self, upc, sorted='none'):
        if sorted=='none':
            retval = self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc)).all()
        elif sorted=='purchase':
            retval = self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc))\
                .order_by(InventoryItem.purchaseDate).all()
            
        return retval
    
    def returnItemByIdentifier (self, identifier):
        return self.session.query(InventoryItem).filter(InventoryItem.identifier.startswith(identifier)).all()
        
    def removeItem (self, item):
        self.session.delete(item)
        self.session.commit()
    
    def searchItem (self, upc):
        return self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc)).count() > 0
    
    def clear (self):
        for item in self.session.query(InventoryItem):
            self.session.delete(item)
        self.session.commit()
    
    def size (self):
        return self.session.quert(InventoryItem).count()
    
    def expiringItems (self, thresholdTime):
        return self.session.query(InventoryItem).filter(InventoryItem.expirationDate > thresholdTime)\
            .order_by(InventoryItem.expirationDate).all()
        
        
    
    