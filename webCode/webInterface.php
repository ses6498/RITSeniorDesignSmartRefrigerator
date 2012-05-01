<HTML>
<HEAD>
<TITLE> Smart Refrigerator </TITLE>
</HEAD>
<BODY>

<?php

   $dbcnx = @mysql_connect("smartfridge.student.rit.edu:3306", "srAdmin", "s3niorD3sign");
   
   if (!$dbcnx){
      die('Could not connect to database server: ' . mysql_error());
   }
     
   mysql_select_db("smartRefrigeratorDb", $dbcnx);         
?>

<h2>Smart Refrigerator Web Interface</h2>

<P><b>Current Inventory Items:</b></P>
<BLOCKQUOTE>

<table border="1">
<tr>
<td><b>Item Description</b></td> 
<td><b>Expiration Date</b></td>
</tr>
<?php
   $inventory = mysql_query("SELECT * FROM inventory");
         
   if (!$inventory){
      die('Error performing query: ' . mysql_error());
   }
      
   while ($row = mysql_fetch_array($inventory)){
      echo ("<tr>");
      echo ("<td>" . $row["description"] . "</td>");
      echo ("<td>" . $row["expirationDate"] . "</td>");
      echo ("</tr>");
   }
?>
</table>
</BLOCKQUOTE>

<P><b>Shopping Lists:</b> Click to view contents</P>
<BLOCKQUOTE>
<table border="1">
<tr>
<td><b>Shopping List Name</b></td>
</tr>
<?php
   $shoppingLists = mysql_query("SELECT * FROM shoppingList");
   
   if (!$shoppingLists){
      die('Error performing query: ' . mysql_error());
   }
   
   while ($row = mysql_fetch_array($shoppingLists)){
      echo ("<tr>");
      echo ("<td><a href=\"shoppingList.php?name=" . $row["name"] . "\">" . $row["name"] . "</a></td>");
      //echo ("<td>" . $row["name"] . "</td>");
      echo ("</tr>");
   }
?>

</table>
</BLOCKQUOTE>
</BODY>
</HTML>