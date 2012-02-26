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
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.util.DataConnect;
import edu.rit.smartFridge.util.TestConnect;

public class ShoppingListActivity extends ListActivity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        DataConnect connecter = new TestConnect();
        List<ShoppingList> lists = connecter.getLists();
        List<String> listNames = new ArrayList<String>();
        
		Iterator<ShoppingList> iter = lists.iterator();
		
		while (iter.hasNext())
		{
			listNames.add(iter.next().getName());
		}
		
		String []a = new String[listNames.size()];
        
        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, listNames.toArray(a)));
        
        ListView lv = getListView();
        lv.setTextFilterEnabled(true);
        
        lv.setOnItemClickListener(new OnItemClickListener()
        {
        	public void onItemClick(AdapterView<?> parent, View view, int position, long id)
        	{
        		// TODO: in here, make the listener open another activity that shows the 
        		// items contained in a list.
        		// Intent intent = new Intent(this, [ActivityName].class)
        		// startActivity(intent)
        		Toast.makeText(getApplicationContext(),((TextView) view).getText() , Toast.LENGTH_SHORT).show();
        	}
        });
    }
}
