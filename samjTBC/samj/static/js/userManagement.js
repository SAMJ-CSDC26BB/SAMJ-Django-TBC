import * as Utils from './utils/utils.js';
import {ButtonBuilder, ElementBuilder} from './builder/builder.js';

const SELECTORS = {
    'editUserButton'            : '.edit-user-btn',
    'deleteUserButton'          : '.delete-user-btn',
    'deleteUserBtnInModal'      : '.uiDeleteUserButton',
    'modalBodyMessage'          : '.modal-body-message',
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
    'dataTableBottom'           : '.dataTable-bottom',
    'passwordInputHelperText'   : '.passwordInputHelperText'
};

const DATA = {
    'editActionMode'          : 'edit',
    'createActionMode'        : 'create',
    'editUserModalTitle'      : 'Edit user',
    'createUserModalTitle'    : 'Create user',
    'bootstrapFormValidated'  : 'was-validated',
    'displayNoneClassName'    : 'd-none'
};

let inEditUserInitialData = {};

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

    userForm.querySelector(SELECTORS.passwordInputHelperText).classList.remove(DATA.displayNoneClassName);

    setFormActionMode(DATA.editActionMode, userForm);

    inEditUserInitialData = {
        username: row.dataset.username,
        fullname: row.dataset.fullname,
        number: row.dataset.number,
        status: row.dataset.status,
        role: row.dataset.role
    };

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
    createNewUser(newUser);
}

function createNewUser(newUser) {
    fetch('/api/user_management/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
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

            Utils.closeModal(SELECTORS.editCreateUserModal);
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
    if (!userForm) {
        return;
    }

    const passwordInput = userForm.querySelector(SELECTORS.passwordInput);
    passwordInput.required = passwordInput.innerText.length > 0;

    if (!userForm.checkValidity()) {
        userForm.classList.add(DATA.bootstrapFormValidated);
        return;
    }

    const updatedUser = getUserDataFromForm(userForm);
    updateUser(updatedUser, isShouldUsePUTRequest(updatedUser));
}

function updateUser(updatedUser, fullUpdate=true) {
    fetch('/api/user_management/', {
        method: fullUpdate ? 'PUT' : 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
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
            afterUpdateUserCallback(updatedUser);
        })
        .catch(error => {
            console.error('Error updating user:', error);
            Utils.showNotificationMessage(`Error updating ${updatedUser.username}`, "error");
        });
}

function afterUpdateUserCallback(updatedUser) {
    Utils.closeModal(SELECTORS.editCreateUserModal);
    Utils.showNotificationMessage(`${updatedUser.username} updated successfully`);
    updateUserInTable(updatedUser);
}

function onDeleteButtonClick(event) {
    const row = getTableRowOfEditedUser(this);

    if (!row) {
        return;
    }

    const username = row.dataset.username;
    const deleteUserModal = document.querySelector(SELECTORS.deleteUserModal);
    if (deleteUserModal) {
        deleteUserModal.querySelector(SELECTORS.modalBodyMessage).innerText
            = deleteUserModal.querySelector(SELECTORS.modalBodyMessage).innerText.replace('{0}', username);

        deleteUserModal.querySelector(SELECTORS.deleteUserBtnInModal).addEventListener('click', (e) => {deleteUser(username, row)});
    }
}

function deleteUser(username, row) {
    fetch('/api/user_management/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
        },
        body: JSON.stringify({username: username})
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            // Check if the response status is 204 (No Content)
            if (response.status === 204) {
                return null;
            }
            return response.json();
        })
        .then(data => {
            Utils.showNotificationMessage(`${username} deleted successfully`, "success");
            Utils.closeModal(SELECTORS.deleteUserModal);
            row.remove();
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            Utils.showNotificationMessage(`Error deleting ${username}`, "error");
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

function isShouldUsePUTRequest(updateUserJSON) {
    return updateUserJSON.fullname !== inEditUserInitialData.fullname
        && updateUserJSON.number !== inEditUserInitialData.number
        && updateUserJSON.status !== inEditUserInitialData.status
        && updateUserJSON.role !== inEditUserInitialData.role;
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