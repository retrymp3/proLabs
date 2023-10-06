<?php
    $arr = array('id'=>007, 'name'=>'admin', 'email'=>'admin@email.com');
    $serialCookie=serialize($arr);


    setcookie("AdminCookie", $serialCookie, time() + 2 * 24 * 60 * 60);
?>
<!DOCTYPE html>
<html>
<body>
    <?php
    class Serial
    {
        private $hook;
     
        function __wakeup()
        {
           if (isset($this->hook)) eval($this->hook);
        }
     }
     
    if (isset($_COOKIE["AdminCookie"]))
    {
        $userdata=unserialize($_COOKIE["AdminCookie"]);
        if ($userdata !== false) {
            $name = $userdata['name'];
            $email = $userdata['email'];
            echo "<b>User Information</b>" . "<br><br>";
            echo "Name: " . $name . "<br>";
            echo "Email: " . $email . "<br>";
        }       
        else {
            echo "Failed to unserialize the cookie data.";
        }
    }
    else
    {
        echo "No user information.";
    }
    function secretFunc()
    {
       echo "<b>flag{0bJ3cT_inJ3cT1on_f04_Th3_WiN}</b>";
    }

    // Call the custom phpinfo() function
    ?>
    <p>
        <strong>Note:</strong>
        You might have to reload the page 
        to see the value of the cookie.
    </p>

</body>
</html>