package edu.rit.smartFridge.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Random;


import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;

public class TestConnect implements DataConnect
{

	/**
	 * auto generated serial version UID
	 */
	private static final long serialVersionUID = 8958256739421033944L;

	ShoppingList list1 = new ShoppingList("List 1", false);
	ShoppingList list2 = new ShoppingList("List 2", false);
	ShoppingList list3 = new ShoppingList("List 3", false);
	ShoppingList list4 = new ShoppingList("List 4", true);

	InventoryItem milk = new InventoryItem("1% Milk", 10, new Date("10/11/12"),
			new Date("10/01/12"));
	InventoryItem bread = new InventoryItem("Wheat Bread", 11, new Date(
			"10/12/12"), new Date("10/02/12"));
	InventoryItem lemons = new InventoryItem("Lemons", 12,
			new Date("10/13/12"), new Date("10/03/12"));
	InventoryItem limes = new InventoryItem("Limes", 13, new Date("10/14/12"),
			new Date("10/04/12"));
	InventoryItem steak = new InventoryItem("T-Bone Steak", 14, new Date(
			"10/15/12"), new Date("10/05/12"));
	InventoryItem cheese = new InventoryItem("Cheddar Cheese", 15, new Date(
			"10/16/12"), new Date("10/06/12"));
	InventoryItem pasta = new InventoryItem("Spaghetti", 16, new Date(
			"10/17/12"), new Date("10/07/12"));
	InventoryItem sauce = new InventoryItem("Pasta Sauce", 17, new Date(
			"10/18/12"), new Date("10/08/12"));
	InventoryItem crackers = new InventoryItem("Ritz Crackers", 18, new Date(
			"10/19/12"), new Date("10/09/12"));
	InventoryItem cereal = new InventoryItem("Cereal", 19,
			new Date("10/20/12"), new Date("10/10/12"));
	InventoryItem juice = new InventoryItem("Orange Juice", 20, new Date(
			"10/21/12"), new Date("10/11/12"));

	InventoryItem[] Inventory = new InventoryItem[]
	{ milk, bread, lemons, limes, steak, cheese, pasta, sauce, crackers,
			cereal, juice };

	public List<ShoppingList> getLists()
	{
		List<ShoppingList> retList = new ArrayList<ShoppingList>();

		retList.add(list1);
		retList.add(list2);
		retList.add(list3);
		retList.add(list4);

		return retList;
	}

	public ShoppingList getList(long listId)
	{
		ShoppingList temp;

		switch ((int) listId)
		{
			case 0:
				temp = list1;
			break;
			case 1:
				temp = list2;
			break;
			case 2:
				temp = list3;
			break;
			case 3:
				temp = list4;
			break;
			default:
				temp = null;
		}

		return temp;
	}

	public ShoppingList populateItems(ShoppingList list)
	{
		Random generator = new Random();
		int size = generator.nextInt(10);
		for (int i = 0; i < size; i++)
		{
			list.addItem(Inventory[generator.nextInt(size)],
					generator.nextInt(3));
		}
		return list;
	}

	public List<InventoryItem> getInventory()
	{
		return Arrays.asList(Inventory);
	}

	public List<InventoryItem> getItem(long UPC)
	{
		List<InventoryItem> retList = new ArrayList<InventoryItem>();

		for (InventoryItem i : Inventory)
		{
			if (i.getUPC() == UPC)
			{
				retList.add(i);
			}
		}
		return retList;

	}

	public int getItemCount(long UPC)
	{
		int count = 0;
		for (InventoryItem i : Inventory)
		{
			if (i.getUPC() == UPC)
			{
				count++;
			}
		}
		return count;
	}

	public List<Date> getExpirationDates(long UPC)
	{
		List<Date> dates = new ArrayList<Date>();
		for (InventoryItem i : Inventory)
		{
			if (i.getUPC() == UPC)
			{
				dates.add(i.getExpiration());
			}
		}

		return dates;
	}

	public List<Date> getPurchaseDates(long UPC)
	{
		List<Date> dates = new ArrayList<Date>();
		for (InventoryItem i : Inventory)
		{
			if (i.getUPC() == UPC)
			{
				dates.add(i.getPurchased());
			}
		}
		return dates;
	}
}
