<h1> Your Details </h1>
<?php

include('../userfiles/'.$_COOKIE["UserDetails"]);
echo '<br>';
echo '....';

?>

<form action="../own7secondpage.php" name="b1">
	<input type="submit" value="Return">
</form>
