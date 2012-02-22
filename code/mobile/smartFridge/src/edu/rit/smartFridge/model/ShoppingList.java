package edu.rit.smartFridge.model;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class ShoppingList {
	private int ID;
	private List<InventoryItem> items;
	private String name;
	private boolean autoGen; // true if the list was created by the item suggester
	
	/**
	 * Shopping List constructor
	 * 
	 * @param name The name of the shopping list
	 */
	public ShoppingList(String name)
	{
		this.name = name;
		autoGen = false;
		items = new ArrayList<InventoryItem>();
	}
	
	/**
	 * Shopping list constructor
	 * 
	 * @param name The name of the shopping list
	 * @param id The ID of the shopping list
	 */
	public ShoppingList(String name, int id)
	{
		this.name = name;
		this.ID = id;
		autoGen = false;
		items = new ArrayList<InventoryItem>();
	}
	
	/**
	 * Gets the ID of the shopping list
	 * 
	 * @return
	 */
	public int getID()
	{
		return ID;
	}
	
	/**
	 * Adds an item to the grocery list
	 * 
	 * @param item The item to add.
	 */
	public void addItem(InventoryItem item)
	{
		items.add(item);
	}
	
	/**
	 * Searches the grocery list for an item with the given name
	 * and returns it.
	 * 
	 * @param name The name of the item to return.
	 * @return The item with the given name.
	 */
	public InventoryItem getItemByName(String name)
	{
		Iterator<InventoryItem> iter = items.iterator();
		InventoryItem temp;
		
		while (iter.hasNext())
		{
			temp = iter.next();
			if (temp.getName().equals(name))
			{
				return temp;
			}
		}
		return null;
	}
	
	/**
	 * Searches the grocery list for an item with the given UPC
	 * and returns it.
	 * 
	 * @param UPC The UPC code of the item to return.
	 * @return The item with the given UPC code.
	 */
	public InventoryItem getItemByUPC(int UPC)
	{
		Iterator<InventoryItem> iter = items.iterator();
		InventoryItem temp;
		
		while (iter.hasNext())
		{
			temp = iter.next();
			if (temp.getUPC() == UPC)
			{
				return temp;
			}
		}
		return null;
	}
	
	/**
	 * Gets all items contained in the list
	 * 
	 * @return The list of items
	 */
	public List<InventoryItem> getAllItems()
	{
		return items;
	}
	
	/**
	 * Gets the name of the grocery list.
	 * 
	 * @return The name of the list.
	 */
	public String getName()
	{
		return name;
	}
	
	/**
	 * Gives the grocery list a new name
	 * 
	 * @param newName The new name of the list.
	 */
	public void setName(String newName)
	{
		name = newName;
	}
	
	/**
	 * Returns a boolean representation of whether the list was aut-generated.
	 * 
	 * @return True if the list was auto-generated, false otherwise.
	 */
	public boolean isAutoGen()
	{
		return autoGen;
	}
}
