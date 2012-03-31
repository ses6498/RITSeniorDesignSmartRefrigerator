package edu.rit.smartFridge.model;

import java.io.Serializable;
import java.util.Date;

import com.j256.ormlite.table.DatabaseTable;

@DatabaseTable(tableName = "Item")
public class InventoryItem implements Serializable
{
	/**
	 * auto generated serial version UID
	 */
	private static final long serialVersionUID = 2421444388805545429L;
	
	/**
	 * The Item's UPC Code
	 */
	private int UPC;
	
	/**
	 * The name of the item
	 */
	private String itemName;
	
	/**
	 * The date which the item will probably be expired
	 */
	private Date expiration;
	
	/**
	 * The date the item was purchased
	 */
	private Date purchased;
	
	/**
	 * Gets the item's UPC code
	 * 
	 * @return The UPC code
	 */
	public int getUPC()
	{
		return UPC;
	}
	
	/**
	 * Gets the item's name
	 * 
	 * @return The item's name
	 */
	public String getName()
	{
		return itemName;
	}
	
	/**
	 * No-argument constructor used by ormlite
	 */
	public InventoryItem() {}
	
	/**
	 * {@code InventoryItem} constructor
	 * 
	 * @param name The name of the {@code InventoryItem}
	 * @param UPC The UPC of the {@code InventoryItem}
	 */
	public InventoryItem(String name, int UPC)
	{
		this(name, UPC, null, null);
	}
	
	/**
	 * Item Constructor
	 * 
	 * @param name The name of the Item 
	 * @param UPC The item's UPC code
	 * @param description A description of the Item
	 * @param expiration When the item will expire
	 */
	public InventoryItem(String name, int UPC, Date expiration, Date purchased)
	{
		this.itemName = name;
		this.UPC = UPC;
		this.expiration = expiration;
		this.purchased = purchased;
	}
	
	/**
	 * Gets the item's expiration date
	 * 
	 * @return The expiration date
	 */
	public Date getExpiration()
	{
		return expiration;
	}
	
	/**
	 * Gets the date the item was purchased
	 * 
	 * @return The purchased date
	 */
	public Date getPurchased()
	{
		return purchased;
	}
}


