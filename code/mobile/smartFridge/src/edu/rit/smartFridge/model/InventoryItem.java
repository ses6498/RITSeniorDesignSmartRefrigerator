package edu.rit.smartFridge.model;

import java.io.Serializable;
import java.util.Date;

public class InventoryItem implements Serializable
{
	/**
	 * auto generated serial version UID
	 */
	private static final long serialVersionUID = 2421444388805545429L;
	
	private int UPC;
	private String itemName;
	private String description;
	private Date expiration;
	
	/**
	 * Item Constructor
	 * 
	 * @param name The name of the Item 
	 * @param UPC The item's UPC code
	 * @param description A description of the Item
	 * @param expiration When the item will expire
	 */
	public InventoryItem(String name, int UPC, String description, Date expiration)
	{
		this.itemName = name;
		this.UPC = UPC;
		this.description = description;
		this.expiration = expiration;
	}
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
	 * Gets the item's description
	 * 
	 * @return The item's name
	 */
	public String Description()
	{
		return description;
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
}
