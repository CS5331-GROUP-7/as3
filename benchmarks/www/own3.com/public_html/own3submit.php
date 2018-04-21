<?php

$folder = $_GET["path"];
$file = $_GET["file"];

$filepath = $folder.$file;

echo "Retrieving " . $filepath;

echo "<br>";

echo "<br>";
include($filepath);

?>
