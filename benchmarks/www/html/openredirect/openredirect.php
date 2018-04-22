Redirecting...

<?php

if (isset($_GET['redirect'])) {
    header("Location: " . $_GET['redirect']);
    die();
}

?>
