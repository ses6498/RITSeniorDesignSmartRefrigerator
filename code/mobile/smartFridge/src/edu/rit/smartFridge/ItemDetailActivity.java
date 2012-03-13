package edu.rit.smartFridge;

import android.app.Activity;
import android.os.Bundle;

public class ItemDetailActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        Bundle extras = getIntent().getExtras();
        String name = null;
        if (extras != null)
        {
        	name = extras.getString("ITEM_NAME");
        }
        this.setTitle(name);
    }
}