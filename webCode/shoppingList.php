<HTML>
<HEAD>
<TITLE> Shopping List Display </TITLE>
</HEAD>
<BODY>

<?php
   $name = $_GET['name'];
   
   $dbcnx = @mysql_connect("smartfridge.student.rit.edu:3306", "srAdmin", "s3niorD3sign");
   
   if (!$dbcnx){
      die('Could not connect to database server: ' . mysql_error());
   }
     
   mysql_select_db("smartRefrigeratorDb", $dbcnx);         
?>

<P><b>Shopping List Items:</b></P>
<BLOCKQUOTE>
<?php
echo "<b>" . $name . "</b>";
?>
<table border="1">

<?php
echo "<tr>";
echo "<td><b> Item Description </b></td>";
echo "<td><b> Quantity </b></td>";
echo "</tr>";
?>

<?php
   $ids = mysql_query ("SELECT listId FROM shoppingList WHERE name='$name'");
   $id = mysql_fetch_array($ids);
   $id = $id["listId"];
   
   $listItems = mysql_query ("SELECT * FROM shoppingListLinker WHERE listId='$id'");
   
   if (!$listItems){
      die('Error performing query: ' . mysql_error());
   }
   
   $count = mysql_num_rows($listItems);
   
   if ($count == 0){
      echo ("<tr>");
      echo ("<td><font color=\"RED\"> --Shopping List Empty-- </font></td>");
      echo ("<td></td>");
      echo ("</tr>");
   }
   
   while ($row = mysql_fetch_array($listItems)){
      echo ("<tr>");
      echo ("<td>" . $row["itemDescription"] . "</td>");
      echo ("<td>" . $row["quantity"] . "</td>");
      echo ("</tr>");
   }
?>

</table>
</BLOCKQUOTE>
</BODY>
</HTML>