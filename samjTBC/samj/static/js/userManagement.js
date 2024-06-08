import {initializeVanillaDataTable, showNotificationMessage} from './utils/utils.js';

document.addEventListener('DOMContentLoaded', function() {
    initializeVanillaDataTable('#userTable');
    initializeEvents();
});

function initializeEvents() {
    document.querySelectorAll('.edit-user-btn').forEach(button => {
        button.addEventListener('click', onEditButtonClick);
    });

    document.querySelectorAll('.delete-user-btn').forEach(button => {
        button.addEventListener('click', onDeleteButtonClick);
    });

    document.querySelector('#editCreateUserModal #saveUserBtn').addEventListener('click', onSaveButtonClick);
}

function onEditButtonClick(event) {
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
}

function onDeleteButtonClick(event) {
    let row = getTableRowOfEditedUser(this),
        deleteModalMessage = document.querySelector('.modal-body-message');

    if (!row) {
        return;
    }

    deleteModalMessage.innerText = deleteModalMessage.innerText.replace('{0}', row.dataset.username);
}

function getTableRowOfEditedUser(context) {
    return context.closest('tr');
}

function onSaveButtonClick(event) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('testAjax', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ username: "test", password: "test" })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            showNotificationMessage(data.message);
        })
        .catch(error => {
            document.getElementById('responseMessage').innerText = 'Error creating user: ' + error;
        });

    //document.querySelector('#userForm').submit();
}