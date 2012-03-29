package edu.rit.smartFridge;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.AdapterView.OnItemLongClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.util.Connector;
import edu.rit.smartFridge.util.DataConnect;

public class ItemListActivity extends ListActivity
{
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        final Context context = this;
        HashMap<String, List<InventoryItem>> inventory = null;
        ShoppingList list = null;
        
        // Get the instance of the connecter
        DataConnect connecter = new Connector().getInstance();
        
        // Set true if we got here from a grocery list, 
        // false if it's just the inventory screen
        final boolean fromList;
        
        // get the current list
        Bundle extras = getIntent().getExtras();
        if (extras != null)
        {
        	list = (ShoppingList) extras.getSerializable(getString(R.string.current_list));
        }
        
        // copy somewhere final for the listener to use
    	final ShoppingList finalList = list;
        
        // if no list was passed in, we need to get the inventory ourselves
        if (list == null)
        {
	        inventory = connecter.getInventory();
	        fromList = false;
        }
        else // we got here from a grocery list
        {
        	list = connecter.populateItems(list);
        	inventory = list.getAllItems();
        	
	        // set the list title, if there is one
	        setTitle(list.getName());
	        
	        fromList = true;
        }
        
        // copy the inventory into a final variable, to be accessed in the listener
        final HashMap<String, List<InventoryItem>> finalInventory = inventory;
        final List<String> finalNames = new ArrayList<String>();
        
        // copy the item names into a list for display
		List<String> inventoryNames = new ArrayList<String>();
		for (String s : inventory.keySet())
		{
			finalNames.add(s);
			int count = inventory.get(s).size();
			inventoryNames.add(count + "x | " + s);
		}
		
		// display the names in a list
		String []a = new String[inventoryNames.size()];
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, inventoryNames.toArray(a)));
        
        // event listeners
        ListView lv = getListView();
        lv.setTextFilterEnabled(true);
        lv.setOnItemClickListener(new OnItemClickListener()
        {
        	public void onItemClick(AdapterView<?> parent, View view, int position, long id)
        	{
        		String key = finalNames.get(position);
        		ArrayList<InventoryItem> itemList = (ArrayList<InventoryItem>) finalInventory.get(key);
				Intent i = new Intent().setClass(context, ItemDetailActivity.class)
					  					.putExtra(getString(R.string.current_item), itemList)
					  					.putExtra("itemIndex", position);
			  context.startActivity(i);
        	}
        });
        
        lv.setLongClickable(true);
        lv.setOnItemLongClickListener(new OnItemLongClickListener()
        {
			public boolean onItemLongClick(AdapterView<?> parent, View v, int position, long id) {
				// get the corresponding inventory item
				InventoryItem item = finalInventory.get(finalNames.get(position)).get(0);
				
				if (fromList)
				{
					Intent i = new Intent().setClass(context, ListRemoveActivity.class)
											.putExtra(getString(R.string.current_list), finalList)
											.putExtra(getString(R.string.current_item), item.getName())
											.putExtra(getString(R.string.current_upc), item.getUPC());
					
					context.startActivity(i);
				}
				else
				{
					Intent i = new Intent().setClass(context, ListAddActivity.class)
											.putExtra(getString(R.string.current_item), item.getName())
											.putExtra(getString(R.string.current_upc), item.getUPC());
					
					context.startActivity(i);
				}
				
				return false;
			}
        });
    }
}
