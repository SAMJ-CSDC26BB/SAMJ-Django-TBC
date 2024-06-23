// Function to handle successful authentication
import * as Utils from './utils/utils.js';

document.addEventListener("DOMContentLoaded", function () {
    let errormessage = document.querySelector('.authentication-error-message');
    if (errormessage) {
        Utils.showNotificationMessage(errormessage.innerText, "error");
        errormessage.remove();
    }
});

var passwordField = document.querySelector('#id_password1');
var confirmPasswordField = document.querySelector('#id_password2');
var passwordError = document.querySelector('#passwordError');
var submitButton = document.querySelector('button[type="submit"]');

passwordField.addEventListener('input', validatePasswords);
confirmPasswordField.addEventListener('input', validatePasswords);

function validatePasswords() {
    var password = passwordField.value;
    var confirmPassword = confirmPasswordField.value;

    var errorMessage = validatePassword(password);
    if (errorMessage || password !== confirmPassword) {
        passwordError.textContent = errorMessage || 'Passwords do not match.';
        submitButton.disabled = true;
    } else {
        passwordError.textContent = '';
        submitButton.disabled = false;
    }
}

function validatePassword(password) {
    if (password.length < 8) {
        return 'Password should be at least 8 characters long.';
    }
    if (!/[a-z]/.test(password)) {
        return 'Password should contain at least one lowercase letter.';
    }
    if (!/[A-Z]/.test(password)) {
        return 'Password should contain at least one uppercase letter.';
    }
    if (!/[0-9]/.test(password)) {
        return 'Password should contain at least one digit.';
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        return 'Password should contain at least one special character.';
    }
    return null;
}