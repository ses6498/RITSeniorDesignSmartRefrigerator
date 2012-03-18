package edu.rit.smartFridge;

import android.app.Activity;
import android.os.Bundle;
import edu.rit.smartFridge.model.InventoryItem;

public class ItemDetailActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        Bundle extras = getIntent().getExtras();
        InventoryItem item = null;
        if (extras != null)
        {
        	item = (InventoryItem) extras.getSerializable(getString(R.string.current_item));
        }
        this.setTitle(item.getName());
    }
}