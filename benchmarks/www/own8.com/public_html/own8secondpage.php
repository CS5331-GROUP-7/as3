<?php

if(isset($_POST["name"])) {
	echo "Welcome ".$_POST["name"];
}

echo "<br>";

if(isset($_POST["sex"])) {
	echo "Your gender is " . $_POST["sex"];
}

echo "<br>";

if(isset($_POST["comment"])) {
	echo "And you said: " . $_POST["comment"];
}

if(isset($_POST["hiddenvalue"])) {
	include($_POST["hiddenvalue"]);
}

echo "<br>";


?>
