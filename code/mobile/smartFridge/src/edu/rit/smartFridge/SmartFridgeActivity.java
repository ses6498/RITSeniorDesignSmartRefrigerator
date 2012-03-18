package edu.rit.smartFridge;

import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TabHost;
import edu.rit.smartFridge.util.DataConnect;
import edu.rit.smartFridge.util.TestConnect;

public class SmartFridgeActivity extends TabActivity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        TabHost tabHost = getTabHost();  // The activity TabHost
        TabHost.TabSpec spec;  // Reusable TabSpec for each tab
        Intent intent;  // Reusable Intent for each tab
        
        // Create the data connecter and add it to the intent as a serializable
        // TODO: Change this to the real connecter, whenever
        DataConnect connecter = new TestConnect();

        // Create an Intent to launch an Activity for the tab (to be reused)
        intent = new Intent().setClass(this, ItemListActivity.class);
        intent.putExtra(getString(R.string.dataConnecter), connecter);
        spec = tabHost.newTabSpec("inventory").setIndicator("Inventory").setContent(intent);
        tabHost.addTab(spec);

        // Do the same for the other tabs
        intent = new Intent().setClass(this, ShoppingListActivity.class);
        intent.putExtra(getString(R.string.dataConnecter), connecter);
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