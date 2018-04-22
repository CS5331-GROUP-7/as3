<html>
<body>
Ping a Host

<form id="rce" method="POST">
    Hostname: <input type="text" name="host" value="google.com" />
    <input type="submit" />
</form>
</body>
</html>

<?php

if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
    echo("<pre>");
    passthru("ping -c 1 " . $_POST['host']);
    echo("</pre>");
}

?>
