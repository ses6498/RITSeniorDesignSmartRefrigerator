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
import android.widget.TextView;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.util.DataConnect;

public class ItemListActivity extends ListActivity 
{
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        final Context context = this;
        
        DataConnect connecter = null;
        Bundle extras = getIntent().getExtras();
        if (extras != null)
        {
        	connecter = (DataConnect) extras.getSerializable(getString(R.string.dataConnecter));
        }
        List<InventoryItem> inventory = connecter.getInventory();
        List<String> inventoryNames = new ArrayList<String>();
        
		Iterator<InventoryItem> iter = inventory.iterator();
		
		while (iter.hasNext())
		{
			inventoryNames.add(iter.next().getName());
		}
		
		String []a = new String[inventoryNames.size()];
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, inventoryNames.toArray(a)));
        
        ListView lv = getListView();
        lv.setTextFilterEnabled(true);
        
        lv.setOnItemClickListener(new OnItemClickListener()
        {
        	public void onItemClick(AdapterView<?> parent, View view, int position, long id)
        	{
			  Intent i = new Intent().setClass(context, ItemDetailActivity.class)
					  					.putExtra("ITEM_NAME", ((TextView) view).getText());
			  context.startActivity(i);
      		  //Toast.makeText(getApplicationContext(),
			  //				((TextView) view).getText(), 
			  //				Toast.LENGTH_SHORT).show();
        	}
        });
    }
}
