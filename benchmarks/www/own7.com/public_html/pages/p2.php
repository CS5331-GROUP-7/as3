<html>
<h1> Random Text: </h1>

<body>
<?php
	function genRandom($length = 15) {
		$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
		$charactersLength = strlen($characters);
		$randomString = '';
		for($i = 0; $i < $length; $i++) {
			$randomString .= $characters[rand(0, $charactersLength - 1)];
		}
		return $randomString;
	}

	echo genRandom();

?>

</body>

<form action="../own7secondpage.php" name="b1">
	<input type="submit" value="Return">
</form>