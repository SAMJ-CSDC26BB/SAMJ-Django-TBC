// Function to handle successful login
function handleSuccessfulLogin() {
    alert('Login successful! You can now use our service.');
    // Redirect to the service page
    window.location.href = '/service';
}

// Event listener for login button
document.getElementById('login-button').addEventListener('click', function() {
    // Perform login (this is just a placeholder - replace with your actual login code)
    let loginSuccessful = true; // This should be the result of your login attempt

    if (loginSuccessful) {
        handleSuccessfulLogin();
    } else {
        alert('Login failed. Please try again.');
    }
});

$(document).ready(function() {
    $("#show_hide_password a").on('click', function(event) {
        event.preventDefault();
        if($('#show_hide_password input').attr("type") === "text"){
            $('#show_hide_password input').attr('type', 'password');
            $('#show_hide_password i').addClass( "fa-eye-slash" );
            $('#show_hide_password i').removeClass( "fa-eye" );
        }else if($('#show_hide_password input').attr("type") === "password"){
            $('#show_hide_password input').attr('type', 'text');
            $('#show_hide_password i').removeClass( "fa-eye-slash" );
            $('#show_hide_password i').addClass( "fa-eye" );
        }
    });
});