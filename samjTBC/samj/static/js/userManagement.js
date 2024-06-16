import * as Utils from './utils/utils.js';
import {ElementBuilder, ButtonBuilder} from './builder/builder.js';

const SELECTORS = {
    'editUserButton'            : '.edit-user-btn',
    'deleteUserButton'          : '.delete-user-btn',
    'createUserButton'          : '.create-user-btn',
    'saveUserButton'            : '#saveUserBtn',
    'fullnameInput'             : '#fullname',
    'usernameInput'             : '#username',
    'numberInput'               : '#number',
    'statusInput'               : '#status',
    'roleInput'                 : '#role',
    'passwordInput'             : '#password',
    'tableRow'                  : 'tr',
    'userTable'                 : '#userTable',
    'tableBody'                 : '.uiUserTableBody',
    'editCreateUserModal'       : '#editCreateUserModal',
    'editCreateUserModalTitle'  : '.modal-title',
    'deleteUserModal'           : '#deleteUserModal',
    'csrfToken'                 : "[name=csrfmiddlewaretoken]",
    'tableDataFullname'         : ".tableDataFullname",
    'tableDataNumber'           : ".tableDataNumber",
    'tableDataStatus'           : ".tableDataStatus",
    'tableDataRole'             : ".tableDataRole",
    'userForm'                  : '#userForm',
    'dataTableBottom'           : '.dataTable-bottom'
};

const DATA = {
    'editActionMode'          : 'edit',
    'createActionMode'        : 'create',
    'editUserModalTitle'      : 'Edit user',
    'createUserModalTitle'    : 'Create user',
    'bootstrapFormValidated'  : 'was-validated'
};

document.addEventListener('DOMContentLoaded', function () {
    populateUserTable();
});

function initializeEvents() {
    document.querySelectorAll(SELECTORS.editUserButton).forEach(button => {
        button.addEventListener('click', onEditButtonClick);
    });

    document.querySelectorAll(SELECTORS.deleteUserButton).forEach(button => {
        button.addEventListener('click', onDeleteButtonClick);
    });

    document.querySelectorAll(SELECTORS.createUserButton).forEach(button => {
        button.addEventListener('click', onCreateButtonClick);
    });

    document.querySelector(SELECTORS.saveUserButton).addEventListener('click', onSaveButtonClick);
}

function onEditButtonClick(event) {
    let row = getTableRowOfEditedUser(this),
        userForm = getUserManagementForm();

    if (!userForm || !row) {
        return;
    }

    Utils.resetForm(userForm);
    Utils.toggleRequiredInputsInForm(userForm, false);

    let userNameInput = userForm.querySelector(SELECTORS.usernameInput);
    userNameInput.value = row.dataset.username;
    userNameInput.disabled = true;

    setFormActionMode(DATA.editActionMode, userForm);
    userForm.querySelector(SELECTORS.fullnameInput).value = row.dataset.fullname;
    userForm.querySelector(SELECTORS.numberInput).value = row.dataset.number;
    userForm.querySelector(SELECTORS.statusInput).value = row.dataset.status;
    userForm.querySelector(SELECTORS.roleInput).value = row.dataset.role;
    userForm.querySelector(SELECTORS.passwordInput).value = '';

    setUserManagementModalTitle(DATA.editUserModalTitle);
}

function onCreateButtonClick(event) {
    let userForm = getUserManagementForm();
    if (!userForm) {
        return;
    }

    userForm.querySelector(SELECTORS.usernameInput).disabled = false;

    Utils.resetForm(userForm);
    Utils.toggleRequiredInputsInForm(userForm, true);
    setFormActionMode(DATA.createActionMode, userForm);
    setUserManagementModalTitle(DATA.createUserModalTitle);
}

function onDeleteButtonClick(event) {
    let row = getTableRowOfEditedUser(this),
        deleteModalMessage = document.querySelector('.modal-body-message');

    if (!row) {
        return;
    }

    deleteModalMessage.innerText = deleteModalMessage.innerText.replace('{0}', row.dataset.username);
}

function populateUserTable() {
    fetch('/api/user_management/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=43200', // 12 hours
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (!data.users) {
                throw new Error("Error fetching users");
            }

            addUsersToTable(data.users);
            Utils.initializeVanillaDataTable('#userTable');
            initializeEvents();

        })
        .catch(error => {
            console.log("Error loading users", error);
            Utils.showNotificationMessage('Error loading the users', "error");
        });
}

function addUsersToTable(users) {
    if (!users) {
        return;
    }

    let userTable = document.querySelector(SELECTORS.userTable);
    if (!userTable) {
        throw new Error("Error fetching users, no user table found");
    }
    users.forEach(user => {
        addUserToTable(user);
    });
}

function onSaveButtonClick(event) {
    const form = getUserManagementForm();
    if (!form || !form.dataset.mode) {
        return;
    }

    if (form.dataset.mode === DATA.createActionMode) {
        createUser(form);
    } else {
        editUser(form);
    }
}

function createUser(userForm = getUserManagementForm()) {
    if (!userForm || !userForm.checkValidity()) {
        userForm.classList.add(DATA.bootstrapFormValidated);
        return;
    }

    const newUser = getUserDataFromForm(userForm);

    fetch('/api/user_management/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm(userForm)
        },
        body: JSON.stringify(newUser)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            return response.json();
        })
        .then(data => {

            closeUserManagementModal();
            Utils.showNotificationMessage(`${newUser.username} created successfully`);
            addUserToTable(newUser);
            initializeEvents();

            let tableBottom = document.querySelector(SELECTORS.dataTableBottom);
            // work-around for bottom of the table, it is overlapping with the last inserted row in the table
            if (tableBottom) {
                tableBottom.style='margin-top:50px';
            }

        })
        .catch(error => {
            console.error('Error updating user:', error);
        });
}

function editUser(userForm = getUserManagementForm()) {
    if (!userForm || !userForm.checkValidity()) {
        return;
    }

    const username = userForm.querySelector(SELECTORS.usernameInput).value;
    const updatedUser = getUserDataFromForm(userForm);

    fetch('/api/user_management/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm(userForm)
        },
        body: JSON.stringify(updatedUser)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {

            closeUserManagementModal();
            Utils.showNotificationMessage(`${username} updated successfully`);
            updateUserInTable(updatedUser);

        })
        .catch(error => {
            console.error('Error updating user:', error);
            Utils.showNotificationMessage(`Error updating ${username}`, "error");
        });
}

function addUserToTable(user) {
    let userTable = document.querySelector(SELECTORS.userTable);
    let tableBody = userTable.querySelector(SELECTORS.tableBody);

    let editButton = new ButtonBuilder()
        .class("btn btn-primary btn-sm me-2 edit-user-btn")
        .with("data-bs-target", SELECTORS.editCreateUserModal)
        .with("data-bs-toggle", "modal")
        .text("Edit");
    let deleteButton = new ButtonBuilder("button")
        .class("btn btn-danger btn-sm delete-user-btn")
        .with("data-bs-toggle", "modal")
        .with("data-bs-target", SELECTORS.deleteUserModal)
        .text("Delete");

    let tableRow = new ElementBuilder("tr")
        .attr({
            'data-username': user.username,
            'data-fullname': user.fullname,
            'data-number': user.number,
            'data-status': user.status,
            'data-role': user.role
        })
        .append(new ElementBuilder("td").class("tableDataUsername").text(user.username))
        .append(new ElementBuilder("td").class("tableDataFullname").text(user.fullname))
        .append(new ElementBuilder("td").class("tableDataNumber").text(user.number))
        .append(new ElementBuilder("td").class("tableDataStatus").text(user.status))
        .append(new ElementBuilder("td").class("tableDataRole").text(user.role))
        .append(new ElementBuilder("td").class("tableDataActions").append(editButton).append(deleteButton));

    tableBody.append(tableRow.element);
}

function updateUserInTable(userData) {
    let userTable = document.querySelector(SELECTORS.userTable);
    let updatedUserTableRow = userTable.querySelector(`[data-username='${userData.username}']`);
    if (!updatedUserTableRow) {
        return;
    }

    updatedUserTableRow.dataset.fullname = userData.fullname;
    updatedUserTableRow.dataset.number = userData.number;
    updatedUserTableRow.dataset.status = userData.status;
    updatedUserTableRow.dataset.role = userData.role;

    updatedUserTableRow.querySelector(SELECTORS.tableDataFullname).innerText = userData.fullname;
    updatedUserTableRow.querySelector(SELECTORS.tableDataNumber).innerText = userData.number;
    updatedUserTableRow.querySelector(SELECTORS.tableDataStatus).innerText = userData.status;
    updatedUserTableRow.querySelector(SELECTORS.tableDataRole).innerText = userData.role;
}

function setUserManagementModalTitle(title, userManagementModal = document.querySelector(SELECTORS.editCreateUserModal)) {
    userManagementModal.querySelector(SELECTORS.editCreateUserModalTitle).innerText = title;
}

function getUserManagementForm() {
    return document.querySelector(SELECTORS.userForm);
}

function setFormActionMode(mode, form = getUserManagementForm()) {
    if (form) {
        form.dataset.mode = mode;
    }
}

function closeUserManagementModal() {
    const modalElement = document.querySelector(SELECTORS.editCreateUserModal);
    const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
    if (modalInstance) {
        modalInstance.hide();
    }
}

function getUserDataFromForm(form = getUserManagementForm()) {
    return {
        username: form.querySelector(SELECTORS.usernameInput).value,
        fullname: form.querySelector(SELECTORS.fullnameInput).value,
        password: form.querySelector(SELECTORS.passwordInput).value,
        number: form.querySelector(SELECTORS.numberInput).value,
        status: form.querySelector(SELECTORS.statusInput).value,
        role: form.querySelector(SELECTORS.roleInput).value
    };
}

function getCsrfTokenFromForm(form = getUserManagementForm()) {
    let token = form.querySelector(SELECTORS.csrfToken);
    if (token) {
        return token.value;
    }
    return '';
}

function getTableRowOfEditedUser(context) {
    return context.closest(SELECTORS.tableRow);
}