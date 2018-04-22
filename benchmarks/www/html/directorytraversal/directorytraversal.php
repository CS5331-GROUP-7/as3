<html>

<body>
Here's your cat:

<pre>
<?php
if (isset($_GET['ascii'])) {
    $file_path = "./cats/" . $_GET['ascii'];
    echo(file_get_contents($file_path));
}
?>
</pre>
</body>
</html>
