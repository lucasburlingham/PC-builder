<?php

// Init the database

// import sqlite
$db = new SQLite3('build_configs.db');

// Check if the table exists
$query = "SELECT name FROM sqlite_master WHERE type='table' AND name='build_configs'";
$result = $db->query($query);

if (!$result->fetchArray()) {
	// Table does not exist, create it
	$createTableQuery = "
        CREATE TABLE build_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            config TEXT NOT NULL
        )
    ";
	$db->exec($createTableQuery) or die('Failed to create build_configs table.');
}

// Import the database manager
require_once('db_manager.php');


// Listen for POST request to add a new configuration
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	// Get the name and config from the POST request
	$name = $_POST['name'];
	$config = $_POST['config'];

	// Add the new configuration to the database
	config::add($db, $config, $name);

	// Redirect to the home page selecting the new configuration in the list by title
	header('Location: index.php?config=' . $id);
}
