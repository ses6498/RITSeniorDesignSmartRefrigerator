<?php
   
   $dbcnx = @mysql_connect("smartfridge.student.rit.edu:3306", "srAdmin", "s3niorD3sign");
   
   if (!$dbcnx){
      die('Could not connect to database server: ' . mysql_error());
   }
   
   mysql_select_db("smartRefrigeratorDb", $dbcnx);

   if ($_REQUEST["action"] == "getInventory") {
      $query = mysql_query ("SELECT * FROM inventory");
   } elseif ($_REQUEST["action"] == "getInventoryItemByUpc") {
      $query = mysql_query ("SELECT * FROM inventory WHERE upc=" .
         $_REQUEST["upc"]);
   } elseif ($_REQUEST["action"] == "getShoppingLists") {
      $query = mysql_query ("SELECT * FROM shoppingList");
   } elseif ($_REQUEST["action"] == "getShoppingListById") {
      $query = mysql_query ("SELECT * FROM shoppingListLinker WHERE listId=" .
         $_REQUEST["listId"]);
   }
   
   if (!$query){
      die('Error performing query: ' . mysql_error());
   }
   
   while($row = mysql_fetch_assoc($query))
      $output[]=$row;
      echo $row;
   
   print (json_encode($output));
   
   mysql_close();
?>