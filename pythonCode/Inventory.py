'''
Created on Mar 18, 2012

@author: Steven
'''
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.dialects import mysql

class InventoryItem (object):
    
    def __init__(self, upc, upcString, name, purchaseDate, expirationDate):
        self.upc = upc
        self.upcString = upcString
        self.name = name
        self.purchaseDate = purchaseDate
        self.expirationDate = expirationDate
        self.identifier = None
        
    def __repr__(self):
        return "<Item('%d', '%s')>" % (self.upc, self.name)

class Inventory ():
    '''
    classdocs
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        
        engine = sqlalchemy.create_engine('mysql://ses6498:seNi{}R1)esign@localhost/smartrefrigeratorDB')
        metadata = sqlalchemy.MetaData()
        
        inventoryTable = sqlalchemy.Table('inventory', metadata, \
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True), \
            sqlalchemy.Column('upc', sqlalchemy.BigInteger), \
            sqlalchemy.Column('upcString', sqlalchemy.String(16)), \
            sqlalchemy.Column('name', sqlalchemy.String(128)), \
            sqlalchemy.Column('purchaseDate', sqlalchemy.DateTime), \
            sqlalchemy.Column('expirationDate', sqlalchemy.DateTime), \
            sqlalchemy.Column('identifier', sqlalchemy.String(16)))
        
        metadata.create_all (engine)
        sqlalchemy.orm.mapper(InventoryItem, inventoryTable)
        
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()
        
        # Initial Inventory Addition
        for item in self.session.query(InventoryItem).all():
            model.controllerObj.inventoryAddition (item)
        
#        self.currentInventory = dict()
        
    def addItem (self, item):
        self.session.add(item)
        self.session.commit()
        
    def returnItem (self, upc):
        retval = self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc)).all()
        return retval
        
    def removeItem (self, upc):
        deletedItems = self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc)).all()
        for item in deletedItems:
            self.session.delete(item)
        
        self.session.commit()
        return deletedItems
    
    def searchItem (self, upc):
        return self.session.query(InventoryItem).filter(InventoryItem.upc==long(upc)).count() > 0
    
    def clear (self):
        for item in self.session.query(InventoryItem):
            self.session.delete(item)
        self.session.commit()
    
    def size (self):
        return self.session.quert(InventoryItem).count()
    