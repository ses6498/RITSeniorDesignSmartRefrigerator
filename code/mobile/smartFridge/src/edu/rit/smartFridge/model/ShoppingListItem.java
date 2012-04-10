package edu.rit.smartFridge.model;

import com.j256.ormlite.field.DatabaseField;
import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable(tableName="shoppingListLinker")
public class ShoppingListItem 
{
	/**
	 * The ID of the item
	 */
	@DatabaseField(columnName="itemId")
	private long UPC;
	
	/**
	 * the Name of the item
	 */
	@DatabaseField(columnName="itemDescription")
	private String itemName;
	
	/**
	 * How many of the item are in the list
	 */
	@DatabaseField
	private int quantity;
	
	/**
	 * Empty constructor for ormlite.
	 */
	public ShoppingListItem(){}
	
	/**
	 * {@code ShoppingListItem} constructor.
	 * @param ID The ID of the Item.
	 * @param name The name of the item.
	 * @param quantity How many of the item exist in the list
	 */
	public ShoppingListItem(long UPC, String name, int quantity)
	{
		this.UPC = UPC;
		this.itemName = name;
		this.quantity = quantity;
	}
	
	/**
	 * Fetches the UPC of the {@code ShoppingListItem}
	 * @return The {@code ShoppingListItem} ID
	 */
	public long getUPC()
	{
		return UPC;
	}
	
	/**
	 * Fetches the name of the {@code ShoppingListItem}
	 * @return The name of the {@code ShoppingListItem}
	 */
	public String getName()
	{
		return itemName;
	}

	/**
	 * Fetches the number of {@code ShoppingListItem}s stored in the {@code ShoppingList}
	 * @return The quantity.
	 */
	public int getQuantity()
	{
		return quantity;
	}
}
