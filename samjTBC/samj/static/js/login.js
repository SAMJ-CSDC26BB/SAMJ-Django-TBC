// Function to handle successful authentication
import * as Utils from './utils/utils.js';
import {showMessagesOnDomLoad} from "./utils/utils.js";

document.addEventListener("DOMContentLoaded", function () {
    Utils.showMessagesOnDomLoad('.loginMessage');

    // Get the input fields and the submit button
    let usernameInput = document.querySelector('#username_email_input');
    let passwordInput = document.querySelector('#password_input');

    // Check the input fields whenever their values change
    usernameInput.addEventListener('input', checkInputFields);
    passwordInput.addEventListener('input', checkInputFields);
});

function checkInputFields() {
    let form = this.closest('form');
    if (!form) {
        return;
    }

    let usernameInput = form.querySelector('#username_email_input');
    let passwordInput = form.querySelector('#password_input');
    let submitButton = form.querySelector('[type="submit"]');
    if (!usernameInput || !submitButton || !passwordInput) {
        return;
    }

    submitButton.disabled = !(usernameInput.value && passwordInput.value);
}