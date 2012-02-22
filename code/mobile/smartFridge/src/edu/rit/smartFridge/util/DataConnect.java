package edu.rit.smartFridge.util;

import java.util.List;

import edu.rit.smartFridge.model.*;

public interface DataConnect 
{
	List<ShoppingList> getLists();
	
	ShoppingList getList(int listId);
	
	ShoppingList populateItems(ShoppingList list);
	
	List<InventoryItem> getInventory();
}
