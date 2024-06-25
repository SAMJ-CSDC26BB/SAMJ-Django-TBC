import * as Utils from './utils/utils.js';

document.addEventListener("DOMContentLoaded", function () {
    let messages = document.querySelectorAll('.messages li');
    messages.forEach(function (message) {
        let messageType = message.className.includes('error') ? 'error' : 'success';
        Utils.showNotificationMessage(message.innerText, messageType);
        message.remove();
    });

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