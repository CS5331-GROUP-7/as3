<html>
<body>
<h1>Server Side Code Injection</h1>
<?php

if (!isset($_GET['page'])) {
    $page = "main";
}
else {
    $page = $_GET['page'];
}

chdir("./pages/");
include($page . ".php");

?>
</body>
</html>
