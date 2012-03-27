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
            
    def unknownUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: Unknown UPC " + upc)
        
    def missingUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: Item Not in Inventory " + upc)
        
    def knownUPC (self, upc):
        self.productUPC.set("")
        self.upcLabel.config(text="Product UPC: " + upc)

    def addInventoryItem (self, item):
        self.inventoryTree.insert('', 0, str(item.upc), text=item.description, \
                                  values=['','',''], tag=str(item.upc))
        self.addDuplicateInventoryItem (item, 1)
        
    def addDuplicateInventoryItem (self, item, quantity):
        self.inventoryTree.insert(str(item.upc), 'end', str(item.upc) + str(item.purchaseDate), \
                                  text=item.description, values=['',item.purchaseDate.strftime('%H:%M %a, %d %b'), \
                                                                 item.expirationDate.strftime('%H:%M %a, %d %b')])
        
        self.inventoryTree.item(str(item.upc), values=[str(quantity), '', ''])
        
    def removeInventoryItem (self, item):
        self.inventoryTree.delete(str(item.upc))
        
    def removeDuplicateInventoryItem (self, item, quantity):
        self.inventoryTree.delete(str(item.upc) + str(item.purchaseDate))
        self.inventoryTree.item(str(item.upc), values=[str(quantity), '', ''])
        
    def removeExpirationWarning (self, upc):
        self.expTable.delete(upc)
        
    def expirationWarning (self, upc, severity, update):
        
        color = 'gray'
        if severity < 1:
            color = 'red'
        elif severity < 2:
            color = 'orange'
        elif severity < 3:
            color = 'yellow'
        elif severity < 5:
            color = 'green'
            
        if not update:
            if severity != 1 and severity != -1:
                self.expTable.insert('', 0, str(upc), text=str(upc), values=[str(severity)+' Days'], tag=str(upc))
            else:
                self.expTable.insert('', 0, str(upc), text=str(upc), values=[str(severity)+' Day'], tag=str(upc))
                
            self.expTable.tag_configure(str(upc), foreground=color)
            
            positioned = False
            index = 0
            while not positioned:
                nextItem = self.expTable.next(str(upc))
                if nextItem and len(self.expTable.item(str(nextItem))['values']):
                    expComp = int(self.expTable.item(str(nextItem))['values'][0].split(' ')[0])
                    
                    if expComp < severity:
                        index += 1
                        self.expTable.move(str(upc), '', index)
                    else:
                        positioned = True
                else:
                    positioned = True
                
        else:
            self.expTable.tag_configure(str(upc), foreground=color)
            if severity != 1 and severity != -1:
                self.expTable.item(str(upc), values=[str(severity)+' Days'])
            else:
                self.expTable.item(str(upc), values=[str(severity)+' Day'])
            
            positioned = False
            index = self.expTable.index(str(upc))
            while not positioned:
                prevItem = self.expTable.prev(str(upc))
                if prevItem and len(self.expTable.item(str(prevItem))['values']):
                    expComp = int(self.expTable.item(str(prevItem))['values'][0].split(' ')[0])
                    
                    if expComp > severity:
                        index -= 1
                        self.expTable.move(str(upc), '', index)
                    else:
                        positioned = True
                else:
                    positioned = True
            
    def showItemInfo (self, item):
        self.nameEn.set(item.description)
        self.purEn.set(item.purchaseDate.strftime('%a, %d %b'))
        self.expEn.set(item.expirationDate.strftime('%a, %d %b'))

    def editEntryHandler (self):
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
            
    def checkInHandler (self):
        state = self.controlObj.checkInMode()
        self.checkIn.config(state='disabled')
        self.checkOut.config(state='normal')
        self.markExp.config(state='disabled')
        self.markCon.config(state='disabled')
    
    def checkOutHandler (self):
        state = self.controlObj.checkOutMode()
        self.checkIn.config(state='normal')
        self.checkOut.config(state='disabled')
        
        if state:
            self.markCon.config(state='normal')
            self.markExp.config(state='normal')
        else:
            self.markCon.config(state='disabled')
            self.markExp.config(state='disabled')
        
    def clearHandler (self):
        self.controlObj.clearInventory()
        
    def clearInventory (self):
        children = self.inventoryTree.get_children()
        
        for child in children:
            self.inventoryTree.delete(child)
            
        children = self.expTable.get_children()
        
        for child in children:
            self.expTable.delete(child)
            
    def markConsumedHandle (self):
        self.controlObj.itemConsumed()
        
    def markExpiredHandle (self):
        self.controlObj.itemExpired()
    
    def deleteLastHandle (self):
        self.controlObj.removeLastItem()
        
    def clearLastItem (self):
        self.delEntry.config(state='disabled')
        self.editEntry.config(state='disabled')
        self.markCon.config(state='disabled')
        self.markExp.config(state='disabled')
        self.upcLabel.config(text='Product UPC:')
        self.nameEn.set('')
        self.expEn.set('')
        self.purEn.set('')
        
    def setLastItem (self, state):
        self.delEntry.config(state='normal')
        self.editEntry.config(state='normal')
        
        if state == self.controlObj.CHECK_OUT_MODE:
            self.markCon.config(state='normal')
            self.markExp.config(state='normal')
        else:
            self.markCon.config(state='disabled')
            self.markExp.config(state='disabled')
            
    def duplicateSelected (self, event):
        index = self.selectionTree.index(self.selectionTree.selection()[0])
        self.controlObj.duplicateSelected(self.items[index])
        
        self.prompt.destroy()
        self.root.focus_set()
        
    def duplicateCancelled (self):
        self.clearLastItem()
        self.prompt.destroy()
        
    def duplicatePrompt (self, items):
        self.prompt = tkinter.Toplevel()
        self.prompt.title("Select Item")
        self.prompt.geometry("+%d+%d" % (self.root.winfo_rootx()+180,
                                  self.root.winfo_rooty()+150))
        self.prompt.protocol("WM_DELETE_WINDOW", self.duplicateCancelled)
        self.prompt.grab_set()
        self.prompt.focus_set()
        
        self.items = items
        self.selectionTree = ttk.Treeview(self.prompt, height=5, \
                                          columns=('purchase', 'expiration'))
        self.selectionTree.column('#0', width=190, anchor='e')
        self.selectionTree.column('purchase', width=105, anchor='e')
        self.selectionTree.column('expiration', width=105, anchor='e')
        self.selectionTree.heading('#0', text='Matching Items')
        self.selectionTree.heading('purchase',text='Purchase Date')
        self.selectionTree.heading('expiration',text='Expiration Date')
        self.selectionTree.grid(column=0,row=0,padx=10,pady=(10,2), sticky=('N','S','E'))    
        selectionScroll = ttk.Scrollbar(self.prompt, orient=tkinter.VERTICAL, command=self.selectionTree.yview)
        selectionScroll.grid(column=1, row=0, sticky=('W','N','S'))
        self.selectionTree.configure(yscrollcommand=selectionScroll.set)
        self.selectionTree.configure(selectmode='browse')
        self.selectionTree.bind('<<TreeviewSelect>>', self.duplicateSelected)
        
        for item in items:
            self.selectionTree.insert('', 'end', str(item.upc) + str(item.purchaseDate), \
                                 text=item.description, values=[item.purchaseDate.strftime('%H:%M %a, %d %b'), \
                                 item.expirationDate.strftime('%H:%M %a, %d %b')], tag=str(item.upc) + str(item.purchaseDate))
    
    def ConstructProductEntry (self, productEntry):
        productEntry.grid(column=0, row=0)
        
        PEframe = ttk.Frame(productEntry, relief="sunken", width=800, height=600)
        PEframe.grid(column=0, row=0, columnspan=2, rowspan=1)
        
        rightFrame = ttk.Frame(PEframe)
        rightFrame.grid(column=2, row=0, columnspan=1, rowspan=9, sticky=('N','S'), padx=10, pady=10)
        
        leftFrame = ttk.Frame(PEframe)
        leftFrame.grid(column=0, row=0, columnspan=2, rowspan=9, sticky=('N','S'), padx=10, pady=10)
        
        self.editEntry = ttk.Button(rightFrame, text="Edit Entry", width=20, state='disabled',\
                                    command=self.editEntryHandler)
        self.editEntry.grid(column=0, row=0, rowspan=2, sticky=('E','N','S'), pady=(10,5))
        self.delEntry = ttk.Button(rightFrame, text="Delete Entry", width=20, state='disabled',\
                                   command=self.deleteLastHandle)
        self.delEntry.grid(column=0, row=2, rowspan=2, sticky=('E','N','S'), pady=5)
        self.markCon = ttk.Button(rightFrame, text="Mark as Consumed", width=20, state='disabled',\
                                  command=self.markConsumedHandle)
        self.markCon.grid(column=0, row=4, rowspan=2, sticky=('E','N','S'), pady=5)
        self.markExp = ttk.Button(rightFrame, text="Mark as Expired", width=20, state='disabled',\
                                  command=self.markExpiredHandle)
        self.markExp.grid(column=0, row=6, rowspan=2, sticky=('E','N','S'), pady=5)
        
        self.editState=False
        
        self.radioOnSty = ttk.Style()
        self.radioOnSty.configure('RadioOn.TButton', background='green')
        self.radioOffSty = ttk.Style()
        self.radioOffSty.configure('RadioOff.TButton', background='red', foreground='red')
        
        self.checkIn = ttk.Button(leftFrame, text="Check In", width=20, state='disabled', \
                                  command=self.checkInHandler)
        self.checkIn.grid(column=0, row=0, pady=10)
        
        self.checkOut = ttk.Button(leftFrame, text="Check Out", width=20, state='normal', \
                                   command=self.checkOutHandler)
        self.checkOut.grid(column=1, row=0, pady=10)
        
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
        
        self.inventoryTree = ttk.Treeview(CIframe, height=16, \
                                          columns=('quantity', 'purchase', 'expiration'))
        self.inventoryTree.column('#0', width=300, anchor='e')
        self.inventoryTree.column('quantity', width=90, anchor='e')
        self.inventoryTree.column('purchase', width=105, anchor='e')
        self.inventoryTree.column('expiration', width=105, anchor='e')
        self.inventoryTree.heading('#0', text='Items')
        self.inventoryTree.heading('quantity',text='Item Quantity')
        self.inventoryTree.heading('purchase',text='Purchase Date')
        self.inventoryTree.heading('expiration',text='Expiration Date')
        self.inventoryTree.grid(column=0,row=0,padx=10,pady=(10,2))
        
        clear = ttk.Button(CIframe, text="Clear Inventory", width=50, command=self.clearHandler)
        clear.grid(column=0, row=1, sticky=('E','S','W'), padx=10, pady=(0,10))
        
    def TimeHandlers (self):
        self.root.bind('<Key-F1>', self.key1)
        self.root.bind('<Key-F2>', self.key2)
        self.root.bind('<Key-F3>', self.key3)
        self.root.bind('<Key-F4>', self.key4)
        self.root.bind('<Key-F5>', self.key5)
        self.root.bind('<Key-F6>', self.key6)
        self.root.bind('<Key-F7>', self.key7)
        self.root.bind('<Key-F8>', self.key8)
        self.root.bind('<Key-F9>', self.key9)
        self.root.bind('<Key-F10>', self.key0)
        
    def __init__ (self, controller):
        self.root = tkinter.Tk()
        self.root.title('Smart Refrigerator Application')
    
        notebook = ttk.Notebook(self.root, width=800, height=480)
        
        productEntry = ttk.Frame(notebook)
        shoppingLists = ttk.Frame(notebook)
        currentInventory = ttk.Frame(notebook)
        
        self.ConstructProductEntry(productEntry)
        self.ConstructShoppingList(shoppingLists)
        self.ConstructCurrentInventory(currentInventory)
        
        self.TimeHandlers()
        
        notebook.add(productEntry, text="Product Entry", state="normal")
        notebook.add(shoppingLists, text="Shopping Lists")
        notebook.add(currentInventory, text="Current Inventory")
        notebook.grid(column=0,row=0)
        
        self.controlObj = controller
        
    def mainLoop (self):
        self.root.mainloop()
        
    def key1 (self, event):
        self.controlObj.advanceHour()
        
    def key2 (self, event):
        for lcv in range(2):
            self.controlObj.advanceHour()
        
    def key3 (self, event):
        for lcv in range(3):
            self.controlObj.advanceHour()
        
    def key4 (self, event):
        for lcv in range(4):
            self.controlObj.advanceHour()
        
    def key5 (self, event):
        for lcv in range(5):
            self.controlObj.advanceHour()
        
    def key6 (self, event):
        for lcv in range(6):
            self.controlObj.advanceHour()
        
    def key7 (self, event):
        for lcv in range(7):
            self.controlObj.advanceHour()
        
    def key8 (self, event):
        for lcv in range(8):
            self.controlObj.advanceHour()
        
    def key9 (self, event):
        for lcv in range(9):
            self.controlObj.advanceHour()
        
    def key0 (self, event):
        for lcv in range(10):
            self.controlObj.advanceHour()