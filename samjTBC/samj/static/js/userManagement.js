import {initializeVanillaDataTable, showNotificationMessage} from './utils/utils.js';

document.addEventListener('DOMContentLoaded', function() {
    initializeVanillaDataTable('#userTable');
    addEventListenersOnEditButtonClick();
    addEventListenerOnDeleteButtonClick();
    addEventListenersOnSaveButtonClick();
});

function addEventListenersOnEditButtonClick() {
    document.querySelectorAll('.edit-user-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            let row = getTableRowOfEditedUser(this),
                form = document.querySelector('#userForm');

            if (!form || !row) {
                return;
            }

            let userNameInput = form.querySelector('#username');
            userNameInput.value = row.dataset.username;
            userNameInput.disabled = true;

            form.querySelector('#fullname').value = row.dataset.fullname;
            form.querySelector('#number').value = row.dataset.number;
            form.querySelector('#status').value = row.dataset.status;
            form.querySelector('#role').value = row.dataset.role;
            form.querySelector('#password').value = '';
        });
    });
}

function addEventListenerOnDeleteButtonClick() {
    document.querySelectorAll('.delete-user-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            let row = getTableRowOfEditedUser(this),
                deleteModalMessage = document.querySelector('.modal-body-message');

            if (!row) {
                return;
            }

            deleteModalMessage.innerText = deleteModalMessage.innerText.replace('{0}', row.dataset.username);
        });
    });
}

function getTableRowOfEditedUser(context) {
    return context.closest('tr');
}

function addEventListenersOnSaveButtonClick() {
    let saveButton = document.querySelector('#editCreateUserModal #saveUserBtn');
    if (!saveButton) {
        return;
    }

    saveButton.addEventListener('click', function() {
        document.querySelector('#userForm').submit();
    });
}