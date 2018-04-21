<?php

$page = $_GET["page"];

$page = str_replace("../", "", $page);


echo "Retrieving " . $page;

echo "<br>";

$filename = "webpages/$page";

$file_handler = fopen($filename, "r");

$contents = fread($file_handler, filesize($filename));
fclose($file_handler);
echo $contents."<br>";
?>

<form name="own1form" action="index.php">
<input type="hidden" name="page" value="main">
<input type="submit" value="Reload Page">
</form>
