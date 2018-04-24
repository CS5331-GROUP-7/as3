<?php

#For testing:
#$value = '../../../../../../../../../../../../etc/passwd';
echo 'here';
$value = '../../../../../../../../README';
setcookie("Own4Cookie", $value);
echo $_COOKIE["Own4Cookie"];
?>
<html>
<form action="index.html">
<input type = "submit" value="Return">
</form>
</html>
