<?php


$in = $_GET['in'];

$in = base64_decode($in);

if(strpos($in,'../') !== false) {
	echo "Directory Traversal Detected!";
}else{

	#$replace = '/textname/e%00/i';

	#$in = preg_replace($replace, $_GET['with'], $in);

	#$name = realpath($in);

	#echo $name;
	echo "<br>";

	echo "Retrieving The Text File of: " . $in;
	echo "<br>";
	echo "------------------------";
	echo "<br>";

	echo file_get_contents(urldecode($in));
}
?>
