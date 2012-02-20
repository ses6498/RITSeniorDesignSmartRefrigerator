package edu.rit.smartFridge;

import android.app.ListActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

public class InventoryActivity extends ListActivity 
{
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
		String[] GROCERIES = new String[] {"test 1", "test 2", "test 3"};

        setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item, GROCERIES));
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
