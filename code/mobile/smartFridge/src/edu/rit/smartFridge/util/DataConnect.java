package edu.rit.smartFridge.util;

import java.io.Serializable;
import java.util.List;

import edu.rit.smartFridge.model.*;

public interface DataConnect extends Serializable
{
	List<ShoppingList> getLists();
	
	ShoppingList getList(int listId);
	
	ShoppingList populateItems(ShoppingList list);
	
	List<InventoryItem> getInventory();
}
