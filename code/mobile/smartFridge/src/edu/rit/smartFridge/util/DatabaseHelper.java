package edu.rit.smartFridge.util;

import java.sql.SQLException;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

import com.j256.ormlite.android.apptools.OrmLiteSqliteOpenHelper;
import com.j256.ormlite.dao.Dao;
import com.j256.ormlite.support.ConnectionSource;
import com.j256.ormlite.table.TableUtils;

import edu.rit.smartFridge.model.InventoryItem;
import edu.rit.smartFridge.model.ShoppingList;
import edu.rit.smartFridge.model.ShoppingListItem;

/**
 * Database helper class used to manage the creation and upgrading of your
 * database. This class also usually provides the DAOs used by the other
 * classes.
 */
public class DatabaseHelper extends OrmLiteSqliteOpenHelper
{

	// name of the database file for your application -- change to something
	// appropriate for your app
	private static final String DATABASE_NAME = "smartRefrigeratorDb";
	// any time you make changes to your database objects, you may have to
	// increase the database version
	private static final int DATABASE_VERSION = 1;

	// the DAO objects we use to access the our model
	private Dao<InventoryItem, Integer> inventoryItemDao = null;
	private Dao<ShoppingList, Integer> shoppingListDao = null;
	private Dao<ShoppingListItem, Integer> shoppingListItemDao = null;

	public DatabaseHelper(Context context)
	{
		super(context, DATABASE_NAME, null, DATABASE_VERSION);
	}

	/**
	 * This is called when the database is first created. Usually you should
	 * call createTable statements here to create the tables that will store
	 * your data.
	 */
	@Override
	public void onCreate(SQLiteDatabase db, ConnectionSource connectionSource)
	{
		try
		{
			// create our DAO's
			Dao<InventoryItem, Integer> idao = getInventoryItemDao();
			Dao<ShoppingList, Integer> sldao = getShoppingListDao();
			Dao<ShoppingListItem, Integer> slidao = getShoppingListItemDao();
			Log.d("TEST", "TEST");
		} catch (SQLException e)
		{
			Log.e(DatabaseHelper.class.getName(), "Can't create database", e);
			throw new RuntimeException(e);
		}
	}

	/**
	 * This is called when your application is upgraded and it has a higher
	 * version number. This allows you to adjust the various data to match the
	 * new version number.
	 */
	@Override
	public void onUpgrade(SQLiteDatabase db, ConnectionSource connectionSource,
			int oldVersion, int newVersion)
	{
//		try
//		{
//			Log.i(DatabaseHelper.class.getName(), "onUpgrade");
//			TableUtils.dropTable(connectionSource, SimpleData.class, true);
//			// after we drop the old databases, we create the new ones
//			onCreate(db, connectionSource);
//		} catch (SQLException e)
//		{
//			Log.e(DatabaseHelper.class.getName(), "Can't drop databases", e);
//			throw new RuntimeException(e);
//		}
	}

	/**
	 * Returns the Database Access Object (DAO) for our InventoryItem class. It
	 * will create it or just give the cached value.
	 */
	public Dao<InventoryItem, Integer> getInventoryItemDao()
			throws SQLException
	{
		if (inventoryItemDao == null)
		{
			inventoryItemDao = getDao(InventoryItem.class);
		}
		return inventoryItemDao;
	}

	/**
	 * Returns the Database Access Object (DAO) for our InventoryItem class. It
	 * will create it or just give the cached value.
	 */
	public Dao<ShoppingList, Integer> getShoppingListDao() throws SQLException
	{
		if (shoppingListDao == null)
		{
			shoppingListDao = getDao(ShoppingList.class);
		}
		return shoppingListDao;
	}

	/**
	 * Returns the Database Access Object (DAO) for our InventoryItem class. It
	 * will create it or just give the cached value.
	 */
	public Dao<ShoppingListItem, Integer> getShoppingListItemDao()
			throws SQLException
	{
		if (shoppingListItemDao == null)
		{
			shoppingListItemDao = getDao(ShoppingListItem.class);
		}
		return shoppingListItemDao;
	}

	/**
	 * Close the database connections and clear any cached DAOs.
	 */
	@Override
	public void close()
	{
		super.close();
		inventoryItemDao = null;
		shoppingListDao = null;
		shoppingListItemDao = null;
	}
}
