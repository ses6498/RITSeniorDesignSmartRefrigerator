package edu.rit.smartFridge;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TableRow.LayoutParams;
import android.widget.TextView;
import edu.rit.smartFridge.util.Connector;
import edu.rit.smartFridge.util.DataConnect;

public class ItemDetailActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.item_info);
        
        Bundle extras = getIntent().getExtras();
        DataConnect connecter = Connector.getInstance();
        List<Date> expDateList = null;
        List<Date> prcDateList = null;
        String itemName = "default"; 
        long UPC = 0;
        if (extras != null)
        {
        	itemName = extras.getString(getString(R.string.current_item));
        	UPC = extras.getLong(getString(R.string.current_upc));
        }
    	expDateList = connecter.getExpirationDates(UPC);
    	prcDateList = connecter.getPurchaseDates(UPC);
        
        this.setTitle(connecter.getItemCount(UPC) + " : " + itemName);
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
        
        for (int i = 0; i < expDateList.size(); i++)
        {
	        tr = new TableRow(this);
	        tr.setLayoutParams(new LayoutParams(
	                LayoutParams.FILL_PARENT,
	                LayoutParams.WRAP_CONTENT));
	        
	        // Build the button text
	        builder.append("Purchased ");
	        builder.append(dateFormat.format(expDateList.get(i)));
	        builder.append("    -    Expires ");
	        builder.append(dateFormat.format(prcDateList.get(i)));
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