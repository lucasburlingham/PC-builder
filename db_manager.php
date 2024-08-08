<?php


class config {
	// What we want is a db manager that can:
	// 1. Create a new table
	// 2. Insert a new row containing a build config in JSON format
	// 3. Retrieve all build configs (if any, otherwise return an empty array)
	// 4. Retrieve a specific build config
	// 5. Retreive a list of build configs based on a search term
	// 6. Update a build config
	// 7. Delete a build config
	// 8. Delete all build configs
	// 9. Close the connection

	function __construct($db) {
		// Create a new table
		$query = "CREATE TABLE IF NOT EXISTS build_config (id INTEGER PRIMARY KEY, config_json TEXT, title TEXT, date_created TEXT)";
		$db->exec($query);
		$query = "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, title TEXT, price TEXT, url TEXT, epoch_scraped TEXT)";
		$db->exec($query);
	}


	// Create a new table
	public static function create_table($db) {
		$query = "CREATE TABLE IF NOT EXISTS build_config (id INTEGER PRIMARY KEY, config_json TEXT, title TEXT, date_created TEXT)";
		$db->exec($query);
		$query = "CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, title TEXT, price TEXT, url TEXT, epoch_scraped TEXT)";
		$db->exec($query);
	}

	// Insert a new row containing a build config in JSON format
	public static function add_build($db, $config_json, $title) {
		$date_created = date('Y-m-d H:i:s');
		$query = "INSERT INTO build_config (config_json, title, date_created) VALUES ('$config_json', '$title', '$date_created')";
		$db->exec($query);
	}

	// Retrieve all build configs
	public static function get_all($db) {
		$query = "SELECT * FROM build_config";

		// Execute the query
		$result = $db->query($query) or die('No results found. Please add one and try again.');

		// Fetch all results
		$result = $db->query($query);
		$build_configs = array();
		while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
			$build_configs[] = $row;
		}

		// If there are no build configs, return an empty array
		return $build_configs;
	}

	// Retrieve a specific build config
	public static function get($db, $id) {
		$query = "SELECT * FROM build_config WHERE id = $id";
		$result = $db->query($query);
		$row = $result->fetchArray(SQLITE3_ASSOC);
		return $row;
	}

	// Retreive a list of build configs based on a search term
	public static function search_configs($db, $search_term) {
		$query = "SELECT * FROM build_config WHERE title LIKE '%$search_term%'";
		$result = $db->query($query);
		$build_configs = array();
		while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
			$build_configs[] = $row;
		}
		return $build_configs;
	}

	// Update a build config (only update what is passed in)
	public static function update($db, $id, $config_json, $title) {
		$query = "UPDATE build_config SET config_json = '$config_json', title = '$title' WHERE id = $id";
		$db->exec($query);
	}

	// Delete a build config
	public static function delete($db, $id) {
		$query = "DELETE FROM build_config WHERE id = $id";
		$db->exec($query);
	}

	// Delete all build configs
	public static function delete_all($db) {
		$query = "DELETE FROM build_config";
		$db->exec($query);
	}

	# Get all products
	public static function get_parts($db) {
		$query = "SELECT * FROM products";

		// Execute the query
		$result = $db->query($query) or die('No results found. Please add one and try again.');

		// Fetch all results
		$result = $db->query($query);
		$products = array();
		while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
			$products[] = $row;
		}

		// If there are no build configs, return an empty array
		return $products;
	}

	// Close the connection
	public function __destruct() {
		global $db; // Add this line to access the global $db variable
		// Close the connection
		$db->close();
	}
}