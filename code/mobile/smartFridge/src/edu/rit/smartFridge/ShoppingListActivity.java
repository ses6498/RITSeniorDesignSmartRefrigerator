package edu.rit.smartFridge;

import java.util.ArrayList;
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
import android.widget.TextView;
import android.widget.Toast;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.util.DataConnect;

public class ShoppingListActivity extends ListActivity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final Context context = this;
        
        // get the connecter
        DataConnect connecter = null;
        Bundle extras = getIntent().getExtras();
        if (extras != null)
        {
        	connecter = (DataConnect) extras.getSerializable(getString(R.string.dataConnecter));
        }
        
        // get the shopping lists
        final List<ShoppingList> lists = connecter.getLists();
        
        // copy the list names into another list for display
        List<String> listNames = new ArrayList<String>();
        String label;
        for (ShoppingList l : lists)
        {
        	if (l.isAutoGen()) 
    		{
        		label = "[A]\t" + l.getName();
    		}
        	else
        	{
        		label = "\t" + l.getName();
        	}
        	
			listNames.add(label);
        }
        
		// display the list
		String []a = new String[listNames.size()];
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, listNames.toArray(a)));
        ListView lv = getListView();
        lv.setTextFilterEnabled(true);
        
        // copy the connector somewhere that the listener can use it
        final DataConnect finalConnecter = connecter;
        
        // make a listener
        lv.setOnItemClickListener(new OnItemClickListener()
        {
        	public void onItemClick(AdapterView<?> parent, View view, int position, long id)
        	{
        		// populate the shopping list's items
        		ShoppingList populatedList = finalConnecter.populateItems(lists.get(position));
				Intent i = new Intent().setClass(context, ItemListActivity.class)
					  					.putExtra(getString(R.string.current_list), populatedList)
					  					.putExtra(getString(R.string.dataConnecter), finalConnecter);
			    context.startActivity(i);
        	}
        });
        
        lv.setLongClickable(true);
        lv.setOnItemLongClickListener(new OnItemLongClickListener()
        {

			public boolean onItemLongClick(AdapterView<?> parent, View v, int position, long id) {
      		    Toast.makeText(getApplicationContext(), ((TextView) v).getText(), Toast.LENGTH_SHORT).show();
				return false;
			}
        });
    }
}
