<!DOCTYPE html>
<html>
<head>
	<title>Test Case 11/login</title>
</head>
<body>
	<?php
	if(isset($_GET["file"])&&$_COOKIE["admin"]=="true"){
		include($_GET["file"]);

	}
	else{
		if($_POST['username']=="admin" && $_POST['password']=="admin"){
			setcookie("admin","true"); 
			echo '<form action = "" method = "get">';
			echo '<input type="text" name="file"><br>';
			echo '<input type = "submit" value = "submit">';
		}
		else if($_POST['username']=="user" && $_POST['password']=="user"){
			echo "welcome user<br>";
		}	
		else echo "GO OUT GO OUT WHO ARE YOU!<br>";
	}
?>
			
</body>
</html>
