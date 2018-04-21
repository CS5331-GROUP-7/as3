<?php


if( $_FILES['file']['tmp_name'] != "") 
{
	$ulDir = $_POST['FILE_PATH'];
	$ulFile = $ulDir . basename($_FILES['file']['name']);
	echo $ulFile . "<br>";

#	if(move_uploaded_file($_FILES['file']['tmp_name'], $ulFile)) {
#	echo "Upload Success!";
#}else{
#	echo "Upload Failure!";
#}

}else
{
	die("No file!");
}

?>

<html>
<head>
<title>Uploaded!</title>
</head>
<h2>What you have uploaded: </h2>
<ul>
<li> Sent File: <?php echo $_FILES['file']['name']; ?>
<li> File Size: <?php echo $_FILES['file']['size']; ?> bytes
<li> File Type: <?php echo $_FILES['file']['type']; ?>
</ul>

<h3>File Contents: </h3>
<?php 

if(file_get_contents($ulFile)) {
	echo file_get_contents($ulFile);
}

?>

</body>
</html>

