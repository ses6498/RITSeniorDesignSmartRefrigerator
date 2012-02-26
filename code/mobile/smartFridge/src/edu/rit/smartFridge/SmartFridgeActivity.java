package edu.rit.smartFridge;

import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TabHost;

public class SmartFridgeActivity extends TabActivity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        TabHost tabHost = getTabHost();  // The activity TabHost
        TabHost.TabSpec spec;  // Resusable TabSpec for each tab
        Intent intent;  // Reusable Intent for each tab

        // Create an Intent to launch an Activity for the tab (to be reused)
        intent = new Intent().setClass(this, InventoryActivity.class);
        spec = tabHost.newTabSpec("inventory").setIndicator("Inventory").setContent(intent);
        tabHost.addTab(spec);

        // Do the same for the other tabs
        intent = new Intent().setClass(this, ShoppingListActivity.class);
        spec = tabHost.newTabSpec("lists").setIndicator("Shopping Lists").setContent(intent);
        tabHost.addTab(spec);
        
        // some networking stuff
//        Socket s = new Socket();
//        InetSocketAddress addr = new InetSocketAddress("192.168.6.31", 22);
//        
//        try
//        {
//	        s.bind(null);
//	        s.connect(addr);
//        }
//        catch (Exception e)
//        {
//        	System.out.println(e.getMessage());
//        }
        
        tabHost.setCurrentTab(2);
    }
}