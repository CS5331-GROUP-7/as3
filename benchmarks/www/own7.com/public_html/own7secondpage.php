<?php
session_start();

$user = $_POST['user'];
$password = $_POST['password'];

if(!isset($_SESSION['uid'])){
	if($user != 'own7' || $password != 'own7')  {
		header('Location: https://own7.com');
		die();
	}else{
		$_SESSION['uid'] = $user;
		setcookie("UserDetails", $user.$password);
		setcookie("loggedin", "yes");
	}
}

?>

<html>

<h1> Welcome To own7! </h1>

<form action="/pages/p1.html" name="b1">
	<input type="submit" value="Site Info">
</form>

<form action="/pages/p2.php" name="b2">
	<input type="submit" value="Random Text">
</form>

<form action="/pages/p3.php" name="b3">
	<input type="submit" value="My Info">
</form>


</html>
