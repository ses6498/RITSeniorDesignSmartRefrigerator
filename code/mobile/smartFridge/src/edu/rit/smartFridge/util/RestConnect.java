package edu.rit.smartFridge.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.model.ShoppingListItem;

/**
 * @author ben
 * 
 */
public class RestConnect implements DataConnect
{
	private List<ShoppingList> shoppingLists = null;
	private List<InventoryItem> inventory = null;

	/**
	 * Autogenerated Serial Version UID
	 */
	private static final long serialVersionUID = 7863854967488611507L;

	/**
	 * RestConnect Constructor.
	 */
	public RestConnect()
	{
		shoppingLists = new ArrayList<ShoppingList>();
		inventory = new ArrayList<InventoryItem>();

		// set the connection timeout time
		int connectionTimeout = 30000; // 30 seconds
		HttpParams params = new BasicHttpParams();
		HttpConnectionParams.setConnectionTimeout(params, connectionTimeout);
	}

	/**
	 * Executes an HTTPRequst against the BeagleBoard to retrieve database items
	 * 
	 * @param nvpList Parameter list for the call
	 * @return A JSONArray of returned values
	 */
	private JSONArray getJSON(List<NameValuePair> nvpList)
	{
		JSONArray jArray = null;
		try
		{
			HttpClient h = new DefaultHttpClient();
			HttpPost httppost = new HttpPost(
					"http://smartfridge.student.rit.edu/mobileServer.php");

			httppost.setEntity(new UrlEncodedFormEntity(nvpList));
			HttpResponse response = h.execute(httppost);
			HttpEntity entity = response.getEntity();
			InputStream is = entity.getContent();

			BufferedReader reader = new BufferedReader(new InputStreamReader(
					is, "iso-8859-1"), 8);
			StringBuilder sb = new StringBuilder();
			String line = null;

			while ((line = reader.readLine()) != null)
			{
				sb.append(line + "\n");
			}
			is.close();
			String result = sb.toString();

			jArray = new JSONArray(result);

		}
		catch (JSONException j)
		{
			System.err.println("INVALID JSON: " + j.getMessage());
		}
		catch (IllegalStateException i)
		{
			System.err.println("ILLEGAL STATE: " + i.getMessage());
		}
		catch (IOException e)
		{
			System.err.println("IO EXCEPTION: " + e.getMessage());
		}

		return jArray;
	}
	
	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getLists()
	 */
	public List<ShoppingList> getLists()
	{
		Log.d("RestConnect", "Retrieving lists");
		if (shoppingLists.size() == 0)
		{
			try
			{
				// build name value pairs
				ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
				nameValuePairs.add(new BasicNameValuePair("action",
						"getShoppingLists"));

				// get JSON (execute request)
				JSONArray jArray = getJSON(nameValuePairs);

				// temporary storage
				long listID;
				String listName;
				boolean autoGen;
				
				if (jArray == null)
				{
					// set shoppingLists to null, so the next
					// time we're here, we'll query the DB again.
					shoppingLists = null;
					return shoppingLists;
				}

				for (int i = 0; i < jArray.length(); i++)
				{
					JSONObject jsonData = jArray.getJSONObject(i);
					listID = jsonData.getLong("listId");
					listName = jsonData.getString("name");
					autoGen = jsonData.getBoolean("autoGeneratedFlag");

					shoppingLists.add(new ShoppingList(listName, autoGen,
							listID));
				}
			}
			catch (JSONException j)
			{
				System.err.println("INVALID JSON: " + j.getMessage());
			}
			catch (IllegalStateException i)
			{
				System.err.println("ILLEGAL STATE: " + i.getMessage());
			}
		}

		return shoppingLists;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getList(int)
	 */
	public ShoppingList getList(long listId)
	{
		Log.d("RestConnect", "Retrieving list" + listId);

		List<ShoppingList> list = this.getLists();
		for (ShoppingList l : list)
		{
			if (l.getID() == listId)
			{
				return l;
			}
		}
		return null;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see
	 * edu.rit.smartFridge.util.DataConnect#populateItems(edu.rit.smartFridge
	 * .model.ShoppingList)
	 */
	public ShoppingList populateItems(ShoppingList list)
	{
		Log.d("RestConnect", "Populating list" + list.getID());

		ShoppingList retList = new ShoppingList(list.getName(),
				list.isAutoGen(), list.getID());
		try
		{
			// convert the list ID to a string
			String input = String.valueOf(list.getID());

			// construct name value pairs
			ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
			nameValuePairs.add(new BasicNameValuePair("action",
					"getShoppingListById"));
			nameValuePairs.add(new BasicNameValuePair("listId", input));

			// get json (Execute request)
			JSONArray jArray = getJSON(nameValuePairs);

			// temp storage
			String itemName;
			long UPC;
			int quantity;
			
			if (jArray == null)
			{
				// return the empty list
				return retList;
			}

			// parse for items
			for (int i = 0; i < jArray.length(); i++)
			{
				JSONObject jsonData = jArray.getJSONObject(i);
				itemName = jsonData.getString("itemDescription");
				UPC = jsonData.getLong("itemId");
				quantity = jsonData.getInt("quantity");
				
				retList.addItem(new ShoppingListItem(UPC, itemName, quantity));
			}
		}
		catch (JSONException j)
		{
			System.err.println("INVALID JSON: " + j.getMessage());
		}
		catch (IllegalStateException i)
		{
			System.err.println("ILLEGAL STATE: " + i.getMessage());
		}

		return retList;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getInventory()
	 */
	public List<InventoryItem> getInventory()
	{
		Log.d("RestConnect", "Getting Inventory");

		if (inventory.size() == 0)
		{
			try
			{
				// build name value pairs
				ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
				nameValuePairs.add(new BasicNameValuePair("action",
						"getInventory"));

				// get JSON (Execute request)
				JSONArray jArray = getJSON(nameValuePairs);
				
				if (jArray == null)
				{
					// set inventory to null, so the next time
					// we're in here, we'll query the DB for it again.
					inventory = null;
					return inventory;
				}

				// temp storage
				String itemName;
				long itemUPC;
				Date expiration;
				Date purchased;
				InventoryItem temp;

				DateFormat d = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
				for (int i = 0; i < jArray.length(); i++)
				{
					JSONObject jsonData = jArray.getJSONObject(i);

					// get data from json stream
					itemUPC = jsonData.getLong("upc");
					itemName = jsonData.getString("description");
					expiration = d.parse(jsonData.getString("expirationDate"));
					purchased = d.parse(jsonData.getString("purchaseDate"));

					temp = new InventoryItem(itemName, itemUPC, expiration,
							purchased);

					inventory.add(temp);
				}
			}
			catch (JSONException j)
			{
				System.err.println("INVALID JSON: " + j.getMessage());
			}
			catch (IllegalStateException i)
			{
				System.err.println("ILLEGAL STATE: " + i.getMessage());
			}
			catch (ParseException e)
			{
				System.err.println("INVALID DATE: " + e.getMessage());
			}
		}

		return inventory;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getItem(long)
	 */
	public List<InventoryItem> getItem(long UPC)
	{
		Log.d("RestConnect", "Getting Item" + UPC);

		List<InventoryItem> retList = new ArrayList<InventoryItem>();

		if (inventory.size() == 0)
		{
			// if the inventory hasn't been retrieved yet, get it.
			getInventory();
		}

		for (InventoryItem i : inventory)
		{
			if (i.getUPC() == UPC)
			{
				retList.add(i);
			}
		}

		return retList;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getItemCount(long)
	 */
	public int getItemCount(long UPC)
	{
		Log.d("RestConnect", "Counting Items: " + UPC);
		return getItem(UPC).size();
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getExpirationDates(long)
	 */
	public List<Date> getExpirationDates(long UPC)
	{
		Log.d("RestConnect", "Getting Expiration Dates" + UPC);

		List<InventoryItem> list = this.getItem(UPC);
		List<Date> retList = new ArrayList<Date>();
		for (InventoryItem i : list)
		{
			if (!retList.contains(i.getExpiration()))
			{
				retList.add(i.getExpiration());
			}
		}
		return retList;
	}

	/*
	 * (non-Javadoc)
	 * 
	 * @see edu.rit.smartFridge.util.DataConnect#getPurchaseDates(long)
	 */
	public List<Date> getPurchaseDates(long UPC)
	{
		Log.d("RestConnect", "Getting Purchase Dates" + UPC);

		List<InventoryItem> list = this.getItem(UPC);
		List<Date> retList = new ArrayList<Date>();
		for (InventoryItem i : list)
		{
			if (!retList.contains(i.getPurchased()))
			{
				retList.add(i.getPurchased());
			}
		}
		return retList;
	}

	public List<ShoppingList> refreshLists()
	{
		shoppingLists = new ArrayList<ShoppingList>();
		return getLists();
	}

	public List<InventoryItem> refreshInventory()
	{
		inventory = new ArrayList<InventoryItem>();
		return getInventory();
	}

}
