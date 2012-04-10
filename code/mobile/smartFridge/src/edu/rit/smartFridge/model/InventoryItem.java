package edu.rit.smartFridge.model;

import java.io.Serializable;
import java.util.Date;

import com.j256.ormlite.field.DatabaseField;
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
	@DatabaseField
	private long UPC;
	
	/**
	 * The name of the item
	 */
	@DatabaseField(columnName="Description")
	private String itemName;
	
	/**
	 * The date which the item will probably be expired
	 */
	@DatabaseField(columnName="expirationDate")
	private Date expiration;
	
	/**
	 * The date the item was purchased
	 */
	@DatabaseField(columnName="purchaseDate")
	private Date purchased;
	
	/**
	 * Gets the item's UPC code
	 * 
	 * @return The UPC code
	 */
	public long getUPC()
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
	 * @param l The UPC of the {@code InventoryItem}
	 */
	public InventoryItem(String name, long l)
	{
		this(name, l, null, null);
	}
	
	/**
	 * Item Constructor
	 * 
	 * @param name The name of the Item 
	 * @param UPC The item's UPC code
	 * @param description A description of the Item
	 * @param expiration When the item will expire
	 */
	public InventoryItem(String name, long UPC, Date expiration, Date purchased)
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


