package edu.rit.smartFridge;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import android.app.ListActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.util.DataConnect;
import edu.rit.smartFridge.util.TestConnect;

public class InventoryActivity extends ListActivity 
{
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        
        DataConnect connecter = new TestConnect();
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
        		Toast.makeText(getApplicationContext(),((TextView) view).getText() , Toast.LENGTH_SHORT).show();
        	}
        });
    }
}
