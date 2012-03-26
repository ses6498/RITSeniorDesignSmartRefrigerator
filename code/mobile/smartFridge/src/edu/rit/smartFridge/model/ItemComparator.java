package edu.rit.smartFridge.model;

import java.util.Comparator;
import java.util.Date;

public class ItemComparator implements Comparator<InventoryItem>
{
	/**
	 * Compares two {@code InventoryItem}s.
	 * 
	 * @param item1 One of the {@code InventoryItem}s to compare
	 * @param item2 The other {@code InventoryItem}s to compare
	 * 
	 * @return +1 if item1 expires before item2, -1 if item2 expires first, 0 otherwise.
	 */
	public int compare(InventoryItem item1, InventoryItem item2) {
		Date expiration1 = item1.getExpiration();
		Date expiration2 = item2.getExpiration();
		
		if (expiration1.before(expiration2))
		{
			return +1;
		}
		else if (expiration1.after(expiration2))
		{
			return -1;
		}
		else
		{
			return 0;
		}
	}
}
