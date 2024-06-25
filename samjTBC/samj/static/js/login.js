// Function to handle successful authentication
import * as Utils from './utils/utils.js';

document.addEventListener("DOMContentLoaded", function () {
        let errormessage = document.querySelector('.authentication-error-message');
        if (errormessage) {
            Utils.showNotificationMessage(errormessage.innerText, "error");
            errormessage.remove();
        }
    }
)
;

$(document).ready(function () {
    $('.toast').toast('show');
});

document.addEventListener("DOMContentLoaded", function () {
    let errormessage = document.querySelector('.authentication-error-message');
    if (errormessage) {
        Utils.showNotificationMessage(errormessage.innerText, "error");
        errormessage.remove();
    }

    // Get the input fields and the submit button
    let usernameInput = document.querySelector('#username_email_input');
    let passwordInput = document.querySelector('#password_input');
    let submitButton = document.querySelector('#submit');

    // Function to check if both fields are filled
    function checkInputFields() {
        if (usernameInput.value && passwordInput.value) {
            submitButton.disabled = false;
        } else {
            submitButton.disabled = true;
        }
    }

    // Check the input fields initially
    checkInputFields();

    // Check the input fields whenever their values change
    usernameInput.addEventListener('input', checkInputFields);
    passwordInput.addEventListener('input', checkInputFields);
});

$(document).ready(function () {
    $('.toast').toast('show');
});