<!DOCTYPE html>
<html>
<head>
    <title>login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="../css/login.css">
</head>
<body>
<div class="container">

<div class="card">

<div class="inner-box" id="card">

<div class="card-front">
    <h2>LOGIN</h2>
    <form action="includes/login-check.php" method="POST">
        <input type="email" class="input-box" placeholder="your Email" name="email" 
        <?php 
        if(isset($_GET['email']) && $page == 'login') {
            echo "value='".$_GET['email']."'";
            } ?>
        required>
        <?php
        if(isset($_GET["email_error_"])) {
            echo "<p class='error'>".$_GET['email_error_']."</p>";
        }
        ?>

        <input type="Password" class="input-box" placeholder="your Password" name="password" required>
        <?php
        if(isset($_GET['pass_error_'])) {
            echo "<p class='error'>".$_GET['pass_error_']."</p>";
        }
        if(isset($_GET['sql_error_'])) {
            echo "<p class='error'>".$_GET['sql_error_']."</p>";
        }
        ?>

        <button type="submit" name="submit" class="submit-btn">Login</button>
        <input type="checkbox"><span>Remember Me</span>
    </form>
    <button type="button" class="submit-btn" onclick="Register()">I'm New Here</button>
</div>

<div class="card-back">
    <h2>Register</h2>
    <form action="includes/regester-check.php" method="POST">

        <input type="text" class="input-box" placeholder="Enter your Name" name="username" 
        <?php 
        if(isset($_GET['username'])) {
            echo "value='".$_GET['username']."'";
            } ?>
        required>
        <?php
        if(isset($_GET['username_error'])) {
            echo "<p class='error'>".$_GET['username_error']."</p>";
        }
        ?>

        <input type="text" class="input-box" placeholder="Enter your Phone number" name="phone_number" 
        <?php 
        if(isset($_GET['phone_number'])) {
            echo "value='".$_GET['phone_number']."'";
            } ?>
        required>
        <?php
        if(isset($_GET['phonenumber_error'])) {
            echo "<p class='error'>".$_GET['phonenumber_error']."</p>";
        }
        ?>

        <input type="email" class="input-box" placeholder="Enter your Email" name="email" 
        <?php 
        if(isset($_GET['email']) && $page == 'regester') {
            echo "value='".$_GET['email']."'";
            } ?>

        required>
        <?php
        if(isset($_GET["email_error"])) {
            echo "<p class='error'> Email already taken</p>";
        }
        ?>

        <input type="Password" class="input-box" placeholder="Enter your Password" name="password" required>
        <?php
        if(isset($_GET['pass_error'])) {
            echo "<p class='error'>".$_GET['pass_error']."</p>";
        }
        ?>

        <input type="Password" class="input-box" placeholder="Confirm your Password" name="re_password" required>
        <?php
        if(isset($_GET['re_pass_error'])) {
            echo "<p class='error'>".$_GET['re_pass_error']."</p>";
        }
        if(isset($_GET['sql_error'])) {
            echo "<p class='error'>".$_GET['sql_error']."</p>";
        }
        if(isset($_GET['errors'])) {
            echo "<p class='error'>".$_GET['errors']."</p>";
        }
        ?>

        <button type="submit" name="submit" class="btn">Register</button>
    </form>
    <a onclick="Login()">Already have an account ?</a>
</div>

</div>
</div>
</div>

<script>
    var card = document.getElementById('card');

    function Register(){
        card.style.transform = "rotateY(-180deg)";
    }
    function Login(){
        card.style.transform = "rotateY(0deg)";
        }
    <?php
    if($page == 'regester') {
        echo "Register();";
    }
    ?>
</script>

</body>
</html>
