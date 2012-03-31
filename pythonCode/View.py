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
        
    def updateTemperature (self, temperature):
        self.temperature.configure(text='Current Temperature: ' + '{:.2F}'.format(temperature) + 'F')
        
    def updateHumidity (self, humidity):
        self.humidity.configure(text='Current Humidity: ' + '{:.2F}'.format(humidity) + '%')
        
    def inventoryContextMenu (self, e, arg):
        self.inventoryTree.focus(arg)
        self.inventoryTree.selection_set(arg)
        self.inventoryContext.post(e.x_root, e.y_root)
        self.contextItem = arg

    def addInventoryItem (self, item):
        self.inventoryTree.insert('', 0, str(item.upc), text=item.description, \
                                  values=['','',''], tag=str(item.upc))
        self.addDuplicateInventoryItem (item, 1)
        self.inventoryTree.tag_bind(str(item.upc), '<3>', lambda event, arg=str(item.upc): self.inventoryContextMenu(event, arg))
        
    def addDuplicateInventoryItem (self, item, quantity):
        epoch = int(time.mktime(item.purchaseDate.timetuple()))
        self.inventoryTree.insert(str(item.upc), 'end', str(item.upc)+str(epoch), \
                                  text=item.description, values=['',item.purchaseDate.strftime('%H:%M %a, %d %b'), \
                                  item.expirationDate.strftime('%H:%M %a, %d %b')], tag=str(item.upc)+str(epoch))
        
        item.identifier = str(item.upc)+str(epoch)
        self.inventoryTree.item(str(item.upc), values=[str(quantity), '', ''])
        self.inventoryTree.tag_bind(str(item.upc)+str(epoch), '<3>', lambda event, arg=str(item.upc)+str(epoch): self.inventoryContextMenu(event, arg))
        
    def removeInventoryItem (self, item):
        self.inventoryTree.delete(str(item.upc))
        
    def removeDuplicateInventoryItem (self, item, quantity):
        epoch = int(time.mktime(item.purchaseDate.timetuple()))
        self.inventoryTree.delete(str(item.upc) + str(epoch))
        self.inventoryTree.item(str(item.upc), values=[str(quantity), '', ''])
        
    def removeExpirationWarning (self, item):
        epoch = int(time.mktime(item.purchaseDate.timetuple()))
        self.expTable.delete(str(item.upc)+str(epoch))
        
    def updateExpirationWarning (self, item, severity):
        color = self.colors[severity] if severity in self.colors else 'gray'
        day = ' Days' if severity != 1 and severity != -1 else ' Day'
        epoch = int(time.mktime(item.purchaseDate.timetuple()))
        
        self.expTable.tag_configure(str(item.upc)+str(epoch), foreground=color)
        self.expTable.item(str(item.upc)+str(epoch), values=[str(severity)+day])
       
    def clearExpirationWarnings (self):
        for child in self.expTable.get_children():
            self.expTable.delete(child)
            
    def addExpirationWarning (self, item, severity):
        color = self.colors[severity] if severity in self.colors else 'gray'
        day = ' Days' if severity != 1 and severity != -1 else ' Day'
        epoch = int(time.mktime(item.purchaseDate.timetuple()))
            
        self.expTable.insert('', 'end', str(item.upc)+str(epoch), text=str(item.description),\
                                 values=[str(severity)+day], tag=str(item.upc)+str(epoch))
        self.expTable.tag_configure(str(item.upc)+str(epoch),foreground=color)
    
    def showItemInfo (self, item):
        self.nameEn.set(item.description)
        self.purEn.set(item.purchaseDate.strftime('%H:%M %a, %d %b'))
        self.expEn.set(item.expirationDate.strftime('%H:%M %a, %d %b'))

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
            
    def shoppingListContextMenu (self, e, arg):
        self.shoppingListTree.focus(arg)
        self.shoppingListTree.selection_set((arg,))
        self.shoppingListContext.post(e.x_root, e.y_root)
            
    def shoppingListItemContextMenu (self, e, arg):
        self.shoppingListTree.focus(arg)
        self.shoppingListTree.selection_set((arg,))
        self.shoppingListItemContext.post(e.x_root, e.y_root)
            
    def addNewShoppingList (self, shoppingList):
        self.shoppingListTree.insert('', 'end', str(shoppingList.listId), text=shoppingList.name,\
                                     values=['', shoppingList.creationDate.strftime('%H:%M %a, %d %b')],\
                                     tag=[str(shoppingList.listId)])
        shoppingList.identifier = str(shoppingList.listId)
        self.shoppingListCascade.add_command(label=shoppingList.name, command = lambda x=shoppingList.listId : self.addToSlContextHandler(x))
        self.inventoryContext.entryconfigure(self.shoppingListMenuIndex, state='normal')
        self.shoppingListTree.tag_bind(shoppingList.identifier, '<3>', lambda event, arg=shoppingList.identifier: self.shoppingListContextMenu(event, arg))
        
    def addNewShoppingListItem (self, linker):
        self.shoppingListTree.insert(str(linker.listId), 0, str(linker.listId)+str(linker.itemDescription),\
                                     text=linker.itemDescription, values=[str(linker.quantity), ''], \
                                     tag=[str(linker.listId)+str(linker.itemDescription)])
        linker.identifier = str(linker.listId)+str(linker.itemDescription)
        self.shoppingListTree.tag_bind(linker.identifier, '<3>', lambda event, arg=linker.identifier: self.shoppingListItemContextMenu(event, arg))
        
    def updateShoppingListItem (self, linker):
        self.shoppingListTree.item(linker.identifier, text=linker.itemDescription, values=[str(linker.quantity), ''])
        
    def createShoppingList (self):
        self.controlObj.createShoppingList(self.slName.get())
        self.slPrompt.destroy()
    
    def createSuggestedShoppingList (self):
        self.controlObj.createSuggestedShoppingList()
        
    def createCustomShoppingListItem (self):
        sel = self.shoppingListTree.selection()[0]
        if self.shoppingListTree.parent(sel): sel = self.shoppingListTree.parent(sel)
        
        self.controlObj.createCustomShoppingListItem (sel,\
                self.slAddName.get(), int(self.slAddQuan.get()))
        self.slAddPrompt.destroy()
        
    def updateCustomShoppingListItem (self):
        sel = self.shoppingListTree.selection()[0]
        name = self.slUpdateName.get()
        quantity = int(self.slUpdateQuan.get())
        self.controlObj.updateShoppingListItemHandler(sel, name, quantity)
        
        self.slUpdatePrompt.destroy()
            
    def removeShoppingListHandler (self):
        self.controlObj.removeShoppingListHandler (self.shoppingListTree.selection()[0])
        
    def removeShoppingListItemHandler (self):
        self.controlObj.removeShoppingListItemHandler (self.shoppingListTree.selection()[0])
        
    def removeShoppingList (self, shoppingList):
        self.shoppingListTree.delete(shoppingList.identifier)
        self.shoppingListCascade.delete(shoppingList.identifier)
        
    def removeShoppingListItem (self, shoppingListItem):
        self.shoppingListTree.delete(shoppingListItem.identifier)
        
    def updateShoppingListItemHandler (self):
        item = self.controlObj.returnItemInfo(self.shoppingListTree.selection()[0])
        self.shoppingListUpdatePrompt(item.itemDescription, item.quantity)
        
    def expItemContextHandler (self):
        self.controlObj.itemExpired(identifier=self.contextItem)
        
    def conItemContextHandler (self):
        self.controlObj.itemConsumed(identifier=self.contextItem)
        
    def addToSlContextHandler (self, listIdentifier):
        self.controlObj.createShoppingListItem (listIdentifier, self.contextItem)
        
    def enableDeleteHandler (self, event):
        self.delList.configure(state='normal')
        self.addItem.configure(state='normal')
    
    def shoppingListAdditionPrompt (self):
        self.slAddPrompt = tkinter.Toplevel()
        self.slAddPrompt.title("Enter Item Information")
        self.slAddPrompt.geometry("+%d+%d" % (self.root.winfo_rootx()+210,
                                  self.root.winfo_rooty()+180))
        self.slAddPrompt.grab_set()
        self.slAddPrompt.focus_set()
        self.slAddLabel = ttk.Label(self.slAddPrompt, text="Enter Item Description and Quantity")
        self.slAddLabel.grid(column=0, columnspan=2, row=0, padx=10, pady=(10,0), sticky=('W'))
        self.slAddNLabel = ttk.Label(self.slAddPrompt, text="Description: ")
        self.slAddNLabel.grid(column=0, row=1, padx=10, pady=(10,2), sticky=('W'))
        self.slAddQLabel = ttk.Label(self.slAddPrompt, text="Quantity: ")
        self.slAddQLabel.grid(column=1, row=1, padx=10, pady=(10,2), sticky=('W'))
        self.slAddName = tkinter.StringVar("")
        self.slAddQuan = tkinter.StringVar("")
        self.slAddQuan.set('1')
        self.slAddNEntry = ttk.Entry(self.slAddPrompt, width=40, textvariable=self.slAddName)
        self.slAddNEntry.grid(column=0,row=2, padx=10)
        self.slAddQEntry = ttk.Entry(self.slAddPrompt, width=20, textvariable=self.slAddQuan)
        self.slAddQEntry.grid(column=1,row=2, padx=10)
        self.slAddButton = ttk.Button(self.slAddPrompt, text="Add Item to Shopping List", width=50,\
                                   command=self.createCustomShoppingListItem)
        self.slAddButton.grid(column=0, columnspan=2, row=3, padx=10, pady=(10,10))    

    def shoppingListUpdatePrompt (self, name, quantity):
        self.slUpdatePrompt = tkinter.Toplevel()
        self.slUpdatePrompt.title("Enter Item Information")
        self.slUpdatePrompt.geometry("+%d+%d" % (self.root.winfo_rootx()+210,
                                  self.root.winfo_rooty()+180))
        self.slUpdatePrompt.grab_set()
        self.slUpdatePrompt.focus_set()
        self.slUpdateLabel = ttk.Label(self.slUpdatePrompt, text="Enter Item Description and Quantity")
        self.slUpdateLabel.grid(column=0, columnspan=2, row=0, padx=10, pady=(10,0), sticky=('W'))
        self.slUpdateNLabel = ttk.Label(self.slUpdatePrompt, text="Description: ")
        self.slUpdateNLabel.grid(column=0, row=1, padx=10, pady=(10,2), sticky=('W'))
        self.slUpdateQLabel = ttk.Label(self.slUpdatePrompt, text="Quantity: ")
        self.slUpdateQLabel.grid(column=1, row=1, padx=10, pady=(10,2), sticky=('W'))
        self.slUpdateName = tkinter.StringVar("")
        self.slUpdateName.set(name)
        self.slUpdateQuan = tkinter.StringVar("")
        self.slUpdateQuan.set(quantity)
        self.slUpdateNEntry = ttk.Entry(self.slUpdatePrompt, width=40, textvariable=self.slUpdateName)
        self.slUpdateNEntry.grid(column=0,row=2, padx=10)
        self.slUpdateQEntry = ttk.Entry(self.slUpdatePrompt, width=20, textvariable=self.slUpdateQuan)
        self.slUpdateQEntry.grid(column=1,row=2, padx=10)
        self.slUpdateButton = ttk.Button(self.slUpdatePrompt, text="Update Item", width=50,\
                                   command=self.updateCustomShoppingListItem)
        self.slUpdateButton.grid(column=0, columnspan=2, row=3, padx=10, pady=(10,10)) 
        
    def shoppingListPrompt (self):
        self.slPrompt = tkinter.Toplevel()
        self.slPrompt.title("Enter Shopping List Name")
        self.slPrompt.geometry("+%d+%d" % (self.root.winfo_rootx()+210,
                                  self.root.winfo_rooty()+180))
        self.slPrompt.grab_set()
        self.slPrompt.focus_set()
        self.slLabel = ttk.Label(self.slPrompt, text="Enter Shopping List Name")
        self.slLabel.grid(column=0, row=0, padx=10, pady=(10,0), sticky=('W'))
        self.slName = tkinter.StringVar("")
        self.slEntry = ttk.Entry(self.slPrompt, width=50, textvariable=self.slName)
        self.slEntry.grid(column=0,row=1, padx=10, pady=10)
        self.slButton = ttk.Button(self.slPrompt, text="Add Shopping List", width=50,\
                                   command=self.createShoppingList)
        self.slButton.grid(column=0, row=2, padx=10, pady=(0,10))
    
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
        self.editEntry.grid(column=0, row=0, sticky=('E','N','S'), pady=(10,5))
        self.delEntry = ttk.Button(rightFrame, text="Delete Entry", width=20, state='disabled',\
                                   command=self.deleteLastHandle)
        self.delEntry.grid(column=0, row=1, sticky=('E','N','S'), pady=5)
        self.markCon = ttk.Button(rightFrame, text="Mark as Consumed", width=20, state='disabled',\
                                  command=self.markConsumedHandle)
        self.markCon.grid(column=0, row=2, sticky=('E','N','S'), pady=5)
        self.markExp = ttk.Button(rightFrame, text="Mark as Expired", width=20, state='disabled',\
                                  command=self.markExpiredHandle)
        self.markExp.grid(column=0, row=3, sticky=('E','N','S'), pady=5)
        self.temperature = ttk.Label(rightFrame, text='Current Temperature:')
        self.temperature.grid(column=0, row=4, sticky=('W'),pady=10)
        self.humidity = ttk.Label(rightFrame, text='Current Humidity:')
        self.humidity.grid(column=0, row=5, sticky=('W'),pady=(0,10))
        
        self.editState=False
        
        self.radioOnSty = ttk.Style()
        self.radioOnSty.configure('RadioOn.TButton', background='green')
        self.radioOffSty = ttk.Style()
        self.radioOffSty.configure('RadioOff.TButton', background='red', foreground='red')
        
        self.checkIn = ttk.Button(leftFrame, text="Check In", width='20', state='disabled', \
                                  command=self.checkInHandler)
        self.checkIn.grid(column=0, row=0, pady=10)
        
        self.checkOut = ttk.Button(leftFrame, text="Check Out", width='20', state='normal', \
                                   command=self.checkOutHandler)
        self.buttonStyle = ttk.Style()
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
        self.expTable.configure(selectmode='browse')
        
    def ConstructShoppingListContextMenu (self, frame):
        self.shoppingListContext = tkinter.Menu(frame)
        self.shoppingListContext.add_command(label='Delete List', command=self.removeShoppingListHandler)
        
    def ConstructShoppingListItemContextMenu (self, frame):
        self.shoppingListItemContext = tkinter.Menu(frame)
        self.shoppingListItemContext.add_command(label='Delete Item', command=self.removeShoppingListItemHandler)
        self.shoppingListItemContext.add_command(label='Edit Item', command=self.updateShoppingListItemHandler)
        self.shoppingListItemContext.add_command(label='Delete List', command=self.removeShoppingListHandler)
        
    def ConstructShoppingList (self, shoppingLists):
        shoppingLists.grid(column=0, row=0)
        
        SLframe = ttk.Frame(shoppingLists, relief="sunken", width=800, height=600)
        SLframe.grid(column=0, row=0, columnspan=2, rowspan=1)
        
        self.root.option_add('*tearOff', False)
        self.ConstructShoppingListContextMenu(SLframe)        
        self.ConstructShoppingListItemContextMenu(SLframe)        
        
        rightFrame = ttk.Frame(SLframe)
        rightFrame.grid(column=2, row=0, columnspan=1, rowspan=4, sticky=('N','S'), padx=10, pady=10)
        
        leftFrame = ttk.Frame(SLframe)
        leftFrame.grid(column=0, row=0, columnspan=1, rowspan=4, sticky=('N','S'), padx=10, pady=10)     
        
        self.shoppingListTree = ttk.Treeview(leftFrame, height=18, columns=('quantity', 'modified'))
        self.shoppingListTree.column('quantity', width=100, anchor='e')
        self.shoppingListTree.column('modified', width=100, anchor='e')
        self.shoppingListTree.column('#0', width=250, anchor='w')
        self.shoppingListTree.heading('quantity', text='Quantity')
        self.shoppingListTree.heading('modified', text='Date Modified')
        self.shoppingListTree.heading('#0', text='Shopping Lists')
        self.shoppingListTree.grid(column=0,row=0)
        self.shoppingListTree.configure(selectmode='browse')
        self.shoppingListTree.bind('<<TreeviewSelect>>', self.enableDeleteHandler)
        
        newList = ttk.Button(rightFrame, text="New List", width=20, command=self.shoppingListPrompt)
        newList.grid(column=0, row=0, sticky=('E','N','S'), pady=(10,5))
        sugList = ttk.Button(rightFrame, text="Suggest List", width=20, command=self.createSuggestedShoppingList)
        sugList.grid(column=0, row=1, sticky=('E','N','S'), pady=5)
        self.delList = ttk.Button(rightFrame, text="Delete List", width=20, state='disabled',\
                                  command=self.removeShoppingListHandler)
        self.delList.grid(column=0, row=2, sticky=('E','N','S'), pady=5)
        self.addItem = ttk.Button(rightFrame, text="Add Item", width=20, state='disabled',\
                                  command=self.shoppingListAdditionPrompt)
        self.addItem.grid(column=0, row=3, sticky=('E','N','S'), pady=5)
        
    def ConstructInventoryContextMenu (self, frame):
        self.inventoryContext = tkinter.Menu(frame)
        self.shoppingListCascade = tkinter.Menu(self.inventoryContext)
        self.inventoryContext.add_command(label='Mark Expired', command=self.expItemContextHandler)
        self.inventoryContext.add_command(label='Mark Consumed', command=self.conItemContextHandler)
        self.shoppingListMenuIndex = 3
        self.inventoryContext.add_cascade(menu=self.shoppingListCascade, label='Add to Shopping List')
        self.inventoryContext.entryconfigure(self.shoppingListMenuIndex, state='disabled')
        
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
        self.inventoryTree.configure(selectmode='browse')
        
        self.root.option_add('*tearOff', False)
        self.ConstructInventoryContextMenu(CIframe)
        
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
      
    def rootDelete (self):
        self.controlObj.terminate()
        self.root.destroy()
        
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
        self.root.bind('<Shift-A>', self.adminKey)
        self.colors = dict()
        self.colors[1] = 'red'
        self.colors[2] = 'orange'
        self.colors[3] = 'yellow'
        self.colors[4] = 'green'
        self.colors[5] = 'green'
        
        notebook.add(productEntry, text="Product Entry", state="normal")
        notebook.add(shoppingLists, text="Shopping Lists")
        notebook.add(currentInventory, text="Current Inventory")
        notebook.grid(column=0,row=0)
        
        self.root.protocol("WM_DELETE_WINDOW", self.rootDelete)
        
        self.controlObj = controller
        
    def mainLoop (self):
        self.root.mainloop()
        
    def adminClearHistory (self):
        self.controlObj.clearHistory()
        
    def adminInitializeUpcLut (self):
        self.controlObj.populateUpcLut()
        
    def adminInitializeGs1Lut (self):
        self.controlObj.populateGs1Lut()
        
    def adminKey (self, event):
        self.admin = tkinter.Toplevel()
        self.admin.title('Administrator Panel')
        self.admin.geometry("+%d+%d" % (self.root.winfo_rootx()+210,
                                  self.root.winfo_rooty()+180))
        self.admin.grab_set()
        self.admin.focus_set()
        self.historyButton = ttk.Button(self.admin, text='Clear History Table', width=50,
                                        command=self.adminClearHistory)
        self.historyButton.grid(column=0, row=0, padx=10, pady=5)
        self.initializeUpcLut = ttk.Button(self.admin, text='Initialize UPC LUT', width=50,
                                        command=self.adminInitializeUpcLut)
        self.initializeUpcLut.grid(column=0, row=1, padx=10, pady=5)
        self.initializeGs1Lut = ttk.Button(self.admin, text='Initialize GS1 LUT', width=50,
                                        command=self.adminInitializeGs1Lut)
        self.initializeGs1Lut.grid(column=0, row=2, padx=10, pady=5)
        
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