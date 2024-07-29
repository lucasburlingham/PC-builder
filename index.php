<?php

// import sqlite
$db = new SQLite3('path_to_your_database.db');

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


// DB manager
require_once('db_manager.php');

// Initially get all build configs from the database and store each row in an array
$build_configs = config::get_all($db);

foreach ($build_configs as $build_config) {
	// Print the title of each build config
	echo $build_config['title'] . '<br>';
}



// If a specific build config is requested, get it from the database
if (isset($_GET['config'])) {
	$id = $_GET['config'];
	$build_config = config::get($db, $id);
	echo 'Title: ' . $build_config['title'] . '<br>';
	echo 'Config: ' . $build_config['config'] . '<br>';
}
?>


<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>PC Configuration Builder</title>
	<!-- <link rel="stylesheet" href="assets/style.css">
	<script src="assets/script.js"></script> -->

	<!-- Include bootstrap 5.3.3 bundled JS and CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</head>

<body>

<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">PC Build Picker</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="add_config.php">Add Config</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search titles" aria-label="Search">
        <button class="btn btn-outline-secondary" type="submit">Submit</button>
      </form>
    </div>
  </div>
</nav>

</body>

</html>