package edu.rit.smartFridge.util;

import java.util.List;

import edu.rit.smartFridge.model.*;

public interface DataConnect 
{
	List<ShoppingList> getLists();
	
	ShoppingList getList(int listId);
	
	List<InventoryItem> getItems(ShoppingList list);
}
