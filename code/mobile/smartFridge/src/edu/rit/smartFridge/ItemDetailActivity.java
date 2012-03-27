package edu.rit.smartFridge;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TableRow.LayoutParams;
import android.widget.TextView;
import edu.rit.smartFridge.model.InventoryItem;

public class ItemDetailActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.item_info);
        
        Bundle extras = getIntent().getExtras();
        //InventoryItem item = null;
        List<InventoryItem> test = null;
        String itemName = "default"; 
        if (extras != null)
        {
        	test = (ArrayList<InventoryItem>) extras.getSerializable(getString(R.string.current_item));
        }
        //this.setTitle(item.getName());
        
        if (test == null)
        {
        	this.setTitle(itemName);
        }
        else
        {
	        this.setTitle(test.size() + " : " + test.get(0).getName());
        }
        TextView t = (TextView) findViewById(R.id.text);
        t.setText("Description: \t");
        
        // user friendly date formatting
        SimpleDateFormat dateFormat = new SimpleDateFormat("MM/dd/yyyy");
        
        // get the table and create some reusable row and button variables
        TableLayout table = (TableLayout) findViewById(R.id.tableLayout);
        TableRow tr = null;
        Button b = null;
        
        // for building the label on each button
        StringBuilder builder = new StringBuilder();
        String label;
        
        for (InventoryItem i : test)
        {
	        tr = new TableRow(this);
	        tr.setLayoutParams(new LayoutParams(
	                LayoutParams.FILL_PARENT,
	                LayoutParams.WRAP_CONTENT));
	        
	        // Build the button text
	        builder.append("Purchased ");
	        builder.append(dateFormat.format(i.getPurchased()));
	        builder.append(";\t Expires ");
	        builder.append(dateFormat.format(i.getExpiration()));
	        label = builder.toString();
	        builder.delete(0, builder.length()); // clear the builder
	        
		    // Create a Button to be the row-content.
		    b = new Button(this);
		    b.setText(label);
		    b.setLayoutParams(new LayoutParams(
		              LayoutParams.FILL_PARENT,
		              LayoutParams.WRAP_CONTENT));
		    
		    // Add Button to row.
		    tr.addView(b);
		    
			// Add row to TableLayout.
			table.addView(tr, new TableLayout.LayoutParams(
			      LayoutParams.FILL_PARENT,
			      LayoutParams.WRAP_CONTENT));
        }
    }
}