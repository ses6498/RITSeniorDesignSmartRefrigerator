package edu.rit.smartFridge;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import android.app.ListActivity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.util.DataConnect;

public class ItemListActivity extends ListActivity 
{
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        final Context context = this;
        List<InventoryItem> inventory = null;
        ShoppingList list = null;
        
        // get the inventory and the dataConnecter
        DataConnect connecter = null;
        Bundle extras = getIntent().getExtras();
        if (extras != null)
        {
        	list = (ShoppingList) extras.getSerializable(getString(R.string.current_list));
        	connecter = (DataConnect) extras.getSerializable(getString(R.string.dataConnecter));
        }
        
        // if no list was passed in, we need to get the inventory ourselves
        if (list == null)
        {
	        inventory = connecter.getInventory();
        }
        else
        {
        	list = connecter.populateItems(list);
        	inventory = list.getAllItems();
        	
	        // set the list title, if there is one
	        setTitle(list.getName());
        }
        
        // copy the item names into a list for display
		Iterator<InventoryItem> iter = inventory.iterator();
        List<String> inventoryNames = new ArrayList<String>();
		while (iter.hasNext()) inventoryNames.add(iter.next().getName());
		
		// display the names in a list
		String []a = new String[inventoryNames.size()];
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, inventoryNames.toArray(a)));
        
        // copy the inventory into a final variable, to be accessed in the listener
        final List<InventoryItem> finalInventory = inventory;
        
        // event listeners
        ListView lv = getListView();
        lv.setTextFilterEnabled(true);
        lv.setOnItemClickListener(new OnItemClickListener()
        {
        	public void onItemClick(AdapterView<?> parent, View view, int position, long id)
        	{
			  Intent i = new Intent().setClass(context, ItemDetailActivity.class)
					  					.putExtra(getString(R.string.current_item), finalInventory.get(position));
			  context.startActivity(i);
      		  //Toast.makeText(getApplicationContext(),
			  //				((TextView) view).getText(), 
			  //				Toast.LENGTH_SHORT).show();
        	}
        });
    }
}
