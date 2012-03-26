package edu.rit.smartFridge.util;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Random;

import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;

public class TestConnect implements DataConnect {

	/**
	 * auto generated serial version UID
	 */
	private static final long serialVersionUID = 8958256739421033944L;
	
	ShoppingList list1 = new ShoppingList("List 1", 1);
	ShoppingList list2 = new ShoppingList("List 2", 2);
	ShoppingList list3 = new ShoppingList("List 3", 3);
	ShoppingList list4 = new ShoppingList("List 4", 4);
	
	InventoryItem milk 		= new InventoryItem("1% Milk", 10, "Tasty milk, from a cow", new Date("10/11/12"));
	InventoryItem bread 	= new InventoryItem("Wheat Bread", 11, "Baked Fresh, sometimes", new Date("10/12/12"));
	InventoryItem lemons 	= new InventoryItem("Lemons", 12, "Yellow and sour", new Date("10/13/12"));
	InventoryItem limes 	= new InventoryItem("Limes", 13, "Like Lemons, only green", new Date("10/14/12"));
	InventoryItem steak 	= new InventoryItem("T-Bone Steak", 14, "Tasty, made of meat", new Date("10/15/12"));
	InventoryItem cheese 	= new InventoryItem("Cheddar Cheese", 15, "Happy cows make happy cheese!", new Date("10/16/12"));
	InventoryItem pasta 	= new InventoryItem("Spaghetti", 16, "Long and thin", new Date("10/17/12"));
	InventoryItem sauce 	= new InventoryItem("Pasta Sauce", 17, "To go with your favorite pasta", new Date("10/18/12"));
	InventoryItem crackers 	= new InventoryItem("Ritz Crackers", 18, "For munching, possibly with cheese", new Date("10/19/12"));
	InventoryItem cereal 	= new InventoryItem("Cereal", 19, "Tasty for breakfast with Milk", new Date("10/20/12"));
	InventoryItem juice 	= new InventoryItem("Orange Juice", 20, "Tasty like milk, except from Oranges", new Date("10/21/12"));
	
	InventoryItem[] Inventory = new InventoryItem[] {milk, bread, lemons, limes, steak, cheese, pasta, sauce, crackers, cereal, juice};
		
	public List<ShoppingList> getLists() {
		List<ShoppingList> retList = new ArrayList<ShoppingList>();
		
		retList.add(list1);
		retList.add(list2);
		retList.add(list3);
		retList.add(list4);
		
		return retList;
	}

	public ShoppingList getList(int listId) {
		ShoppingList temp;
		
		switch(listId)
		{
		case 1: temp = list1;
			break;
		case 2: temp = list2;
			break;
		case 3: temp = list3;
			break;
		case 4: temp = list4;
			break;
		default: temp = null;
		}
		
		return temp;
	}

	public ShoppingList populateItems(ShoppingList list) {
		Random generator = new Random();
		int size = generator.nextInt(10);
		for (int i = 0; i < size; i++)
		{
			list.addItem(Inventory[generator.nextInt(10)]);
		}
		return list;
	}

	public List<InventoryItem> getInventory() {
		List<InventoryItem> retList = new ArrayList<InventoryItem>(Arrays.asList(Inventory));
		return retList;
	}

}
