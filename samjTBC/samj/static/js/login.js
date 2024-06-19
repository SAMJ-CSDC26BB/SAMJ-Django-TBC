// Function to handle successful login
import * as Utils from './utils/utils.js';

document.addEventListener("DOMContentLoaded", function () {
        let errormessage = document.querySelector('.login-error-message');
        let successmessagemessage = document.querySelector('.login-success-message');
        if (errormessage) {
            if (errormessage.innerText.includes("error")) {
                Utils.showNotificationMessage(errormessage.innerText, "error");
            } else if (errormessage.innerText.includes("success")) {
                Utils.showNotificationMessage(errormessage.innerText, "success");
            }
            errormessage.remove();
        }
    }
)
;

$(document).ready(function () {
    $('.toast').toast('show');
});