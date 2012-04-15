package edu.rit.smartFridge.util;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import android.content.Context;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;

public interface DataConnect extends Serializable
{
	List<ShoppingList> getLists();

	ShoppingList getList(int listId);

	ShoppingList populateItems(ShoppingList list);

	List<InventoryItem> getInventory();

	List<InventoryItem> getItem(long UPC);

	int getItemCount(long UPC);

	List<Date> getExpirationDates(long UPC);

	List<Date> getPurchaseDates(long UPC);
}
