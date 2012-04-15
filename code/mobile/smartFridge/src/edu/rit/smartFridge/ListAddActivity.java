package edu.rit.smartFridge;

import java.util.ArrayList;
import java.util.List;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.util.Connector;
import edu.rit.smartFridge.util.DataConnect;

public class ListAddActivity extends ListActivity
{

	/** Called when the activity is first created. */
	public void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);

		// get the extras and the connector
		Bundle extras = getIntent().getExtras();
		DataConnect connector = Connector.getInstance();

		final String itemName;
		final int UPC;

		// get item name and UPC
		if (extras != null)
		{
			itemName = (String) extras
					.getString(getString(R.string.current_item));
			UPC = (int) extras.getInt(getString(R.string.current_upc));
		} else
		{
			itemName = "";
			UPC = -1;
		}

		// get the shopping lists; final so it can be accessed by the event
		// handler
		final List<ShoppingList> lists = connector.getLists();

		// copy the names somewhere they can be displayed
		List<String> listNames = new ArrayList<String>();
		for (ShoppingList l : lists)
		{
			listNames.add(l.getName());
		}

		// display the list
		String[] a = new String[listNames.size()];
		setListAdapter(new ArrayAdapter<String>(this, R.layout.list_item,
				listNames.toArray(a)));
		ListView lv = getListView();
		lv.setTextFilterEnabled(true);

		// make a listener
		lv.setOnItemClickListener(new OnItemClickListener() {
			public void onItemClick(AdapterView<?> parent, View view,
					int position, long id)
			{
				ShoppingList list = lists.get(position);
				list.addItem(new InventoryItem(itemName, UPC), 1);

				Intent i = new Intent(parent.getContext(),
						SmartFridgeActivity.class).putExtra(
						getString(R.string.curr_tab), 0);

				parent.getContext().startActivity(i);
			}
		});
	}

}
