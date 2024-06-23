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