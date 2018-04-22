<html>
<head>

<h1>Secret Messages</h1>

<form method="POST">
    Message: <input type="text" name="secret" value="SECRET" />
    <input type="hidden" name="csrftoken" value="abcdef1235" />
    <input type="submit" />
</form>

<?php

$servername = "localhost";
$username = "root";
$password = "toor";
$db = "csrf";

// Create connection
$conn = new mysqli($servername, $username, $password, $db);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) {

    if (!isset($_POST['csrftoken']) || $_POST['csrftoken'] != "abcdef1235") {
        die("Bad CSRF token.");
    }

    if (isset($_POST['secret'])) {
        $query = "update sensitives set message = '" . $_POST['secret'] . "' where indexno = 1;";
        $conn->query($query);
        echo("<b>Updated</b><br />");
    }
    else {
        die("Bad stuff happened.");
    }
}
else {
    $query = "SELECT message FROM sensitives WHERE indexno = 1";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        echo("<p>Secret Message:</p>");
        while($row = $result->fetch_assoc()) {
            echo("<b>" . $row['message'] . "</b><br />");
        }
    } else {
        echo("Weird thing happened.");
    }

}
$conn->close();

?>
</head>
</html>
