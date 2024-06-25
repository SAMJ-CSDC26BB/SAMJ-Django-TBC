import * as Utils from "./utils/utils";

document.querySelector('#logout-btn').addEventListener('click', function (e) {
    console.log("Logout button clicked");  // Debug line
    e.preventDefault();

    fetch('/logout/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',  // Specify that you want the response in JSON format
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();  // Ensure the response is parsed as JSON
    })
    .then(data => {
        if (data.success) {
            Utils.showNotificationMessage(data.message, "success");
            // Redirect to login page after 2 seconds
            setTimeout(function () {
                window.location.href = '/login/';  // Update this to your login URL
            }, 2000);
        } else {
            Utils.showNotificationMessage(data.message, "error");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Utils.showNotificationMessage(`Error: ${error}`, "error");
    });
});