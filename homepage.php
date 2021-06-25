<!DOCTYPE html>
<html>
<head>
	<title>Bus Management</title>
</head>
<body>
<h1> This is bus management home page</h1>
<p>
<?php
require 'includes/db_lib.php';
$info = get_passager_info($conn, $_SESSION['id']);
update_active($conn, $_SESSION['id']);
if(isset($_SESSION['id'])) {
	echo "Username: ".$info['username']."<br>";
	echo "Phone number: ".$info['phone_number']."<br>";
	echo "Email: ".$info['email']."<br>";
	echo "Regestered date: ".$info['regestered_date']."<br>";
	echo "Last active: ".$info['last_active']."<br>";
}
?>
</p><br>
<a href="?mode=logout">Logout</a>
</body>
</html>