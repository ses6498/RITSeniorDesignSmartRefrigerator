package edu.rit.smartFridge.util;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;

import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;

public interface DataConnect extends Serializable
{
	List<ShoppingList> getLists();
	
	ShoppingList getList(int listId);
	
	ShoppingList populateItems(ShoppingList list);
	
	HashMap<String, List<InventoryItem>> getInventory();
}
