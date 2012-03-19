'''
Created on Mar 10, 2012

@author: Steven
'''

import Tkinter as tkinter
import time
import ttk

class View ():
    
    def UPCEntryHandler(self, event):
        
        try:
            stringIn = self.productUPC.get()
            
            # Type Check
            int(stringIn)
           
            if (len(stringIn) != 12):
                raise ValueError
                
            self.controlObj.upcEntered(stringIn)
            
        except ValueError:
            self.controlObj.upcEntered(stringIn, valid=False)
            
    def invalidUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: Invalid UPC " + upc)
#        self.upcLabel.update(text="Product UPC: Invalid UPC" + upc)
            
    def unknownUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: Unknown UPC " + upc)
        
    def knownUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: " + upc)
#        self.upcLabel.update(text="Product UPC: " + upc)

    def addInventoryItem (self, item):
        self.inventoryTree.insert('', 0, 'item' + str(self.inventoryIdentifier), text=item[1][0], \
                                  values=(str(time.strftime('%a,%d,%b', item[1][2]))))
        self.inventoryIdentifier = self.inventoryIdentifier+1
        
    def showItemInfo (self, info):
        self.nameEn.set(info[0])
        self.purEn.set(time.strftime('%a, %d %b', info[1]))
        self.expEn.set(time.strftime('%a, %d %b', info[2]))

    def editEntryHandler(self):
        print self.editState
        
        self.editState = not self.editState
        
        if self.editState:
            self.editEntry.config(text="Confirm Edit")
            
            self.nameEntry.config(state='normal')
            self.nameLabel.config(state='normal')
            self.purEntry.config(state='normal') 
            self.purLabel.config(state='normal')
            self.expEntry.config(state='normal') 
            self.expLabel.config(state='normal')
        else:
            self.editEntry.config(text="Edit Entry")
            
            self.nameEntry.config(state='readonly')
            self.nameLabel.config(state='disabled')
            self.purEntry.config(state='readonly') 
            self.purLabel.config(state='disabled')
            self.expEntry.config(state='readonly') 
            self.expLabel.config(state='disabled')
    
    def ConstructProductEntry (self, productEntry):
        productEntry.grid(column=0, row=0)
        
        PEframe = ttk.Frame(productEntry, relief="sunken", width=800, height=600)
        PEframe.grid(column=0, row=0, columnspan=2, rowspan=1)
        
        rightFrame = ttk.Frame(PEframe)
        rightFrame.grid(column=2, row=0, columnspan=1, rowspan=9, sticky=('N','S'), padx=10, pady=10)
        
        leftFrame = ttk.Frame(PEframe)
        leftFrame.grid(column=0, row=0, columnspan=2, rowspan=9, sticky=('N','S'), padx=10, pady=10)
        
        self.editEntry = ttk.Button(rightFrame, text="Edit Entry", width=20, command=self.editEntryHandler)
        self.editEntry.grid(column=0, row=0, rowspan=2, sticky=('E','N','S'), pady=(10,5))
        delEntry = ttk.Button(rightFrame, text="Delete Entry", width=20)
        delEntry.grid(column=0, row=2, rowspan=2, sticky=('E','N','S'), pady=5)
        markCon = ttk.Button(rightFrame, text="Mark as Consumed", width=20)
        markCon.grid(column=0, row=4, rowspan=2, sticky=('E','N','S'), pady=5)
        markExp = ttk.Button(rightFrame, text="Mark as Expired", width=20)
        markExp.grid(column=0, row=6, rowspan=2, sticky=('E','N','S'), pady=5)
        
        self.editState=False
        
        self.checkIn = ttk.Button(leftFrame, text="Check In", width=20)
        self.checkIn.grid(column=0, row=0, pady=10)
        checkOut = ttk.Button(leftFrame, text="Check Out", width=20, state='disabled')
        checkOut.grid(column=1, row=0, pady=10)
        
        self.nameEn = tkinter.StringVar("")
        self.purEn = tkinter.StringVar("")
        self.expEn = tkinter.StringVar("")
        
        self.upcLabel = ttk.Label(leftFrame, text="Product UPC:", font=('TkDefaultFont',12))
        self.upcLabel.grid(column=0, row=1, columnspan=2, sticky=('W'), pady=(10,2))
        self.productUPC = tkinter.StringVar()
        upcEntry = ttk.Entry(leftFrame, textvariable=self.productUPC)
        upcEntry.grid(column=0, row=2, columnspan=2, sticky=('W','E'), pady=(0,10))
        upcEntry.bind("<Return>", self.UPCEntryHandler)
        self.nameLabel = ttk.Label(leftFrame, text="Product Name:", width=50, font=('TkDefaultFont',12))
        self.nameLabel.grid(column=0, row=3, columnspan=2, sticky=('W','E'), pady=(0,2))
        self.nameEntry = ttk.Entry(leftFrame, textvariable=self.nameEn)
        self.nameEntry.grid(column=0, row=4, columnspan=2, sticky=('W','E'))
        self.purLabel = ttk.Label(leftFrame, text="Purchase Date:", font=('TkDefaultFont',12))
        self.purLabel.grid(column=0, row=5, pady=(10,2), sticky=('W'))
        self.expLabel = ttk.Label(leftFrame, text="Expiration Date:", font=('TkDefaultFont',12))
        self.expLabel.grid(column=1, row=5, padx=(5,0), pady=(10,2), sticky=('W'))
        self.purEntry = ttk.Entry(leftFrame, textvariable=self.purEn)
        self.purEntry.grid(column=0, row=6, padx=(0,5), sticky=('W','E'))
        self.expEntry = ttk.Entry(leftFrame, textvariable=self.expEn)
        self.expEntry.grid(column=1, row=6, padx=(5,0), sticky=('W','E'))
        
        self.nameEntry.config(state='readonly')
        self.nameLabel.config(state='disabled')
        self.purEntry.config(state='readonly') 
        self.purLabel.config(state='disabled')
        self.expEntry.config(state='readonly') 
        self.expLabel.config(state='disabled')
        
        self.expListLabel = ttk.Label(leftFrame, text="Expiration Warnings:",font=('TkDefaultFont',12))
        self.expListLabel.grid(column=0, row=7, pady=(8,2), columnspan=2, sticky=('W','E'))
        
        self.expTable = ttk.Treeview (leftFrame, height=5, columns=('severity'))
        self.expTable.column('severity', width=100, anchor='w')
        self.expTable.column('#0',width=350, anchor='e')
        self.expTable.heading('severity', text='Severity')
        self.expTable.heading('#0', text='Item')
        self.expTable.grid(column=0, row=8, pady=(8,2), columnspan=2, sticky=('W','E'))
        expScroll = ttk.Scrollbar(leftFrame, orient=tkinter.VERTICAL, command=self.expTable.yview)
        expScroll.grid(column=2, row=8, sticky=('W','N','S'))
        self.expTable['yscrollcommand'] = expScroll.set
        
        self.expTable.insert('', 0, 'w1', text="Third Item Near Exp", values=("3Days"), tag='w1')
        self.expTable.tag_configure('w1', foreground='green')
        self.expTable.insert('', 0, 'w2', text="Second Item Near Exp ", values=("1Day"), tag='w2')
        self.expTable.insert('', 0, 'w3', text="Third Item Near Exp", values=("1Day"), tag='w2')
        self.expTable.tag_configure('w2', foreground='red')
        
#        tree = ttk.Treeview(CIframe, columns=('expiration'))
#        tree.column('expiration', width=100, anchor='e')
#        tree.column('#0', width=500, anchor='e')
#        tree.heading('expiration',text='Expiration Date')
#        tree.heading('#0', text='Items')
#        tree.grid(column=0,row=0,padx=10,pady=10)
#        
#        tree.insert('', 0, 'item1', text='Maxwell House Coffee', values=('A_Week'))
#        tree.insert('', 0, 'item2', text='Bacon', values=('Never'))
#        
#        clear = ttk.Button(CIframe, text="Clear Inventory", width=50)
#        clear.grid(column=0, row=1, sticky=('E','S','W'), padx=10, pady=(0,10))        
        
#        listt=tkinter.StringVar(value=('this is item one', 'CROW I AM GOING TO EXPIRE TOO'))
        
#        self.expList = tkinter.Listbox(leftFrame, listvariable=listt, height=6)
#        self.expList.grid(column=0, row=8, pady=(8,2), columnspan=2, sticky=('W','E','N'))
        
    def ConstructShoppingList (self, shoppingLists):
        shoppingLists.grid(column=0, row=0)
        
        SLframe = ttk.Frame(shoppingLists, relief="sunken", width=800, height=600)
        SLframe.grid(column=0, row=0, columnspan=2, rowspan=1)
        
        rightFrame = ttk.Frame(SLframe)
        rightFrame.grid(column=2, row=0, columnspan=1, rowspan=4, sticky=('N','S'), padx=10, pady=10)
        
        leftFrame = ttk.Frame(SLframe)
        leftFrame.grid(column=0, row=0, columnspan=1, rowspan=4, sticky=('N','S'), padx=10, pady=10)     
        
        tree = ttk.Treeview(leftFrame, height=18, columns=('modified'))
        tree.column('modified', width=100, anchor='e')
        tree.column('#0', width=350, anchor='e')
        tree.heading('modified', text='Date Modified')
        tree.heading('#0', text='Shopping Lists')
        tree.grid(column=0,row=0)
        
        tree.insert('', 0, 'test1', text='Shopping List 1', values=('03/18/12'))
        tree.insert('', 1, 'test2', text='Shopping List 2', values=('03/14/12'))
        
        tree.insert('test1',0,text='Shopping List 1 Item 2')
        tree.insert('test1',0,text='Shopping List 1 Item 1')
        tree.insert('test2',0,text='Shopping List 2 Item 2')
        tree.insert('test2',0,text='Shopping List 2 Item 1')
        
        newList = ttk.Button(rightFrame, text="New List", width=20)
        newList.grid(column=0, row=0, sticky=('E','N','S'), pady=(10,5))
        sugList = ttk.Button(rightFrame, text="Suggested List", width=20)
        sugList.grid(column=0, row=1, sticky=('E','N','S'), pady=5)
        editList = ttk.Button(rightFrame, text="Edit List", width=20)
        editList.grid(column=0, row=2, sticky=('E','N','S'), pady=5)
        delList = ttk.Button(rightFrame, text="Delete List", width=20)
        delList.grid(column=0, row=3, sticky=('E','N','S'), pady=5)
        
    def ConstructCurrentInventory (self, currentInventory):
        currentInventory.grid(column=0, row=0)
        
        CIframe = ttk.Frame(currentInventory, relief="sunken", width=800, height=600)
        CIframe.grid(column=0, row=0, columnspan=1, rowspan=2)
        
        self.inventoryTree = ttk.Treeview(CIframe, height=16, columns=('expiration'))
        self.inventoryTree.column('expiration', width=100, anchor='e')
        self.inventoryTree.column('#0', width=500, anchor='e')
        self.inventoryTree.heading('expiration',text='Expiration Date')
        self.inventoryTree.heading('#0', text='Items')
        self.inventoryTree.grid(column=0,row=0,padx=10,pady=(10,2))
        
#        self.inventoryTree.insert('', 0, 'item1', text='Inventory Item One', values=('03/18/12'))
#        self.inventoryTree.insert('', 0, 'item2', text='Inventory Item Two', values=('05/02/12'))
        
        self.inventoryIdentifier=0
        
        clear = ttk.Button(CIframe, text="Clear Inventory", width=50)
        clear.grid(column=0, row=1, sticky=('E','S','W'), padx=10, pady=(0,10))
        
    def __init__ (self, controller):
        self.root = tkinter.Tk()
        self.root.title('Smart Refrigerator Application')
    
        notebook = ttk.Notebook(self.root)
        
        productEntry = ttk.Frame(notebook)
        shoppingLists = ttk.Frame(notebook)
        currentInventory = ttk.Frame(notebook)
        
        self.ConstructProductEntry(productEntry)
        self.ConstructShoppingList(shoppingLists)
        self.ConstructCurrentInventory(currentInventory)
        
        notebook.add(productEntry, text="Product Entry", state="normal")
        notebook.add(shoppingLists, text="Shopping Lists")
        notebook.add(currentInventory, text="Current Inventory")
        notebook.grid(column=0,row=0)
        
        self.controlObj = controller
        
    def mainLoop (self):
        self.root.mainloop()
        