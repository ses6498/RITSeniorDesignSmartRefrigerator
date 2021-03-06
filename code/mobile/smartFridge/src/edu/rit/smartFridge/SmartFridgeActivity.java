package edu.rit.smartFridge;

import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TabHost;

public class SmartFridgeActivity extends TabActivity
{
	/** Called when the activity is first created. */
	@Override
	public void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.main);

		int tabIndex = 0;

		Bundle extras = getIntent().getExtras();
		if (extras != null)
		{
			tabIndex = extras.getInt(getString(R.string.curr_tab));
		}

		TabHost tabHost = getTabHost(); // The activity TabHost
		TabHost.TabSpec spec; // Reusable TabSpec for each tab
		Intent intent; // Reusable Intent for each tab

		// Create an Intent to launch an Activity for the tab (to be reused)
		intent = new Intent().setClass(this, ItemListActivity.class);
		spec = tabHost.newTabSpec("inventory").setIndicator("Inventory")
				.setContent(intent);
		tabHost.addTab(spec);

		// Do the same for the other tabs
		intent = new Intent().setClass(this, ShoppingListActivity.class);
		spec = tabHost.newTabSpec("lists").setIndicator("Shopping Lists")
				.setContent(intent);
		tabHost.addTab(spec);

		tabHost.setCurrentTab(tabIndex);
	}
}