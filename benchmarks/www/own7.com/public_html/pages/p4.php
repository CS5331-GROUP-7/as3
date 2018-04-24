<html>
<h1> just echo csrf </h1>
<br/>
<body>
<?php
    if(isset($_GET['csrftoken']) && !empty($_GET['csrftoken'])){
        echo "csrftoken = ".$_GET['csrftoken'].'<br/>';
    } else {
        echo "no csrftoken<br/>";
    }

?>

</body>
</html>
