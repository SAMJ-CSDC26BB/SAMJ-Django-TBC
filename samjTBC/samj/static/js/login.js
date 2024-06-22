// Function to handle successful login
import * as Utils from './utils/utils.js';

document.addEventListener("DOMContentLoaded", function () {
        let errormessage = document.querySelector('.login-error-message');
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