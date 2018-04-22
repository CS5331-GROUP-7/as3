<html>

<body>
<h1>User Directory</h1>

Search for user:
<form id="directory" method="POST">
    <input type="text" name="username" />
    <input type="submit" />
</form>
<?php

if ( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
    $servername = "localhost";
    $username = "root";
    $password = "toor";
    $db = "sqli";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $db);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $query = "select username, age, school from users where username = '" . $_POST['username'] . "';";

    if (isset($_GET['debug'])) {
        echo("<pre>" . $query . "</pre><br />");
    }

    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        echo("<p>We found you!</p>");
        while($row = $result->fetch_assoc()) {
            echo("<b>Username: </b>" . $row['username'] . "<br />");
            echo("<b>Age: </b>" . $row['age'] . "<br />");
            echo("<b>School: </b>" . $row['school'] . "<br />");
        }
    } else {
        echo("User not found.");
    }
$conn->close();
}

?>

</body>
</html>
