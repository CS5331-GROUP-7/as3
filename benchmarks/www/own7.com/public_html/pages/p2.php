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
    if(isset($_GET['csrftoken']) && !empty($_GET['csrftoken'])){
        echo "csrftoken = ".$_GET['csrftoken'].'<br/>';
    } else {
        echo "no csrftoken<br/>";
    }
	echo genRandom();

?>

</body>

<form action="p2.php" name="b0">
    <input type="hidden" name="csrftoken" value="<?php echo genRandom()?>"/>
	<input type="submit" value="Submit with csrf">
</form>

<form action="p4.php" name="b1">
    <input type="hidden" name="csrftoken" value="abcdef"/>
	<input type="submit" value="Return">
</form>
