import * as Utils from './utils/utils.js';
import {ButtonBuilder, ElementBuilder} from './builder/builder.js';

const SELECTORS = {
    // Buttons
    createDestinationButton: '#create-destination-btn',
    saveDestinationButton: '#saveDestinationBtn',
    deleteDestinationButton: '.uiDeleteDestinationButton',
    editDestinationButton: '.edit-destination-btn', // Generated edit button for destinations
    deleteDestinationRowButton: '.delete-destination-btn', // Generated delete button for destinations

    // Modals
    editCreateDestinationModal: '#editCreateDestinationModal',
    deleteDestinationModal: '#deleteDestinationModal',
    deleteTbcEntryModal: '#deleteTbcEntryModal',

    // Forms
    destinationForm: '#destinationForm',

    // Form Inputs
    destinationNameInput: '#destinationName',
    destinationNumberInput: '#destinationNumber',

    // Tables
    destinationsTable: '#destinationsTable',
    destinationTableBody: '.uiDestinationTableBody',

    // Misc
    csrfToken: "[name=csrfmiddlewaretoken]",
    modalCloseButton: '.btn-close',
    modalTitle: '.modal-title',
    modalBodyMessage: '.modal-body-message'
};

const DATA = {
    'editActionMode': 'edit',
    'createActionMode': 'create',
    'editDestinationModalTitle': 'Edit Destination',
    'createDestinationModalTitle': 'Create Destination',
    'bootstrapFormValidated': 'was-validated',
    'displayNoneClassName': 'd-none'
};

document.addEventListener('DOMContentLoaded', function () {
    populateDestinationsTable();
});

function initializeEvents() {
    document.querySelectorAll(SELECTORS.editDestinationButton).forEach(button => {
        button.addEventListener('click', onEditButtonClick);
    });

    document.querySelectorAll(SELECTORS.deleteDestinationButton).forEach(button => {
        button.addEventListener('click', onDeleteButtonClick);
    });

    document.querySelectorAll(SELECTORS.createDestinationButton).forEach(button => {
        console.log("create button")
        button.addEventListener('click', onCreateButtonClick);
    });

    document.querySelector(SELECTORS.saveDestinationButton).addEventListener('click', onSaveButtonClick);
    //document.querySelector(SELECTORS.saveDestinationButton).addEventListener('click', onSaveButtonClick);
}


function populateDestinationsTable() {
    console.log("populateDestinationsTable");
    fetch('/api/callingNumberManagement/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=1', // 12 hours
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        //console.log(data.destinations);
        return data;
    })
    .then(data => {
        if (!data.destinations) {
            throw new Error("Error fetching destinations");
        }
        addDestinationsToTable(data.destinations);
        Utils.initializeVanillaDataTable('#destinationsTable');
        initializeEvents();

    })
    .catch(error => {
        console.error(error.message)
        Utils.showNotificationMessage('Error loading the Destination', error.message);
    });
}

function addDestinationsToTable(destinations) {
    if (!destinations) {
        return;
    }

    let destinationsTable = document.querySelector(SELECTORS.destinationsTable);
    if (!destinationsTable) {
        throw new Error("Error fetching destinations, no user table found");
    }
    destinations.forEach(destination => {
        addDestinationToTable(destination);
    });
}

function addDestinationToTable(destination) {
    let destinationsTable = document.querySelector(SELECTORS.destinationsTable);
    let tableBody = destinationsTable.querySelector(SELECTORS.destinationTableBody);

    // Create Edit button
    let editButton = new ButtonBuilder()
        .class("btn btn-primary btn-sm me-2 edit-destination-btn")
        .with("data-bs-target", SELECTORS.editCreateDestinationModal)
        .with("data-bs-toggle", "modal")
        .text("Edit");

    // Create Delete button
    let deleteButton = new ButtonBuilder("button")
        .class("btn btn-danger btn-sm delete-destination-btn")
        .with("data-bs-toggle", "modal")
        .with("data-bs-target", SELECTORS.deleteDestinationModal)
        .text("Delete");

    // Create table row
    let tableRow = new ElementBuilder("tr")
        .attr({
            'data-number': destination.number,
            'data-name': destination.name
        })
        .append(new ElementBuilder("td").class("tableDataNumber").text(destination.number))
        .append(new ElementBuilder("td").class("tableDataName").text(destination.name))
        .append(new ElementBuilder("td").class("tableDataActions").append(editButton).append(deleteButton));

    // Append the constructed row to the table body
    tableBody.append(tableRow.element);
}

function onDeleteButtonClick(event) {
    console.log("delete button pressed")
    const row = getTableRowOfEditedDestination(this);

    if (!row) {
        console.log("no row")
        return;
    }

    const number = row.dataset.number;
    console.log(number)
    const deleteDestinationModal = document.querySelector(SELECTORS.deleteDestinationModal);
    if (deleteDestinationModal) {
        deleteDestinationModal.querySelector(SELECTORS.modalBodyMessage).innerText
            = deleteDestinationModal.querySelector(SELECTORS.modalBodyMessage).innerText.replace('{0}', number);

        deleteDestinationModal.querySelector(SELECTORS.deleteDestinationButton).addEventListener('click', (e) => {deleteDestination(number, row)});
    }
}

function onSaveButtonClick(event) {
    console.log("save Button clicked");
    const form = getDestinationManagementForm();
    if (!form || !form.dataset.mode) {
        return;
    }

    if (form.dataset.mode === DATA.createActionMode) {
        createDestination(form);
    } else {
        editDestination(form);
    }
}

function onCreateButtonClick(event) {
    console.log("create clicked");
    let destinationForm = getDestinationManagementForm();
    if (!destinationForm) {
        return;
    }

    destinationForm.querySelector(SELECTORS.destinationNameInput).disabled = false;

    Utils.resetForm(destinationForm);
    Utils.toggleRequiredInputsInForm(destinationForm, true);
    setFormActionMode(DATA.createActionMode, destinationForm);
    setDestinationManagementModalTitle(DATA.createDestinationModalTitle);
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
    userForm.querySelector(SELECTORS.fullnameInput).value = row.dataset.fullname;
    userForm.querySelector(SELECTORS.numberInput).value = row.dataset.number;
    userForm.querySelector(SELECTORS.statusInput).value = row.dataset.status;
    userForm.querySelector(SELECTORS.roleInput).value = row.dataset.role;
    userForm.querySelector(SELECTORS.passwordInput).value = '';

    setUserManagementModalTitle(DATA.editUserModalTitle);
}

function createDestination(destinationData) {
    fetch('/api/callingNumberManagement/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
        },
        body: JSON.stringify(destinationData),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                fetchDestinations();
                closeModal();
            }
        });
}

function updateDestination(destinationData) {
    fetch('/api/callingNumberManagement/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(destinationData),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                fetchDestinations();
                closeModal();
            }
        });
}

function deleteDestination(destinationData) {
    fetch('/api/destination_management/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({id: destinationData.id}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                fetchDestinations();
                closeModal();
            }
        });
}


function fillForm(destination) {
    const form = document.querySelector(SELECTORS.destinationForm);
    form.querySelector('#destinationName').value = destination.name;
    form.querySelector('#destinationNumber').value = destination.number;
}

function clearForm() {
    const form = document.querySelector(SELECTORS.destinationForm);
    form.reset();
}

function closeModal() {
    const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
    if (modal) {
        modal.hide();
    }
}


function getDestinationManagementForm() {
    return document.querySelector((SELECTORS.destinationForm))
}

function getCsrfTokenFromForm(form = getDestinationManagementForm()) {
    let token = form.querySelector(SELECTORS.csrfToken);
    if (token) {
        return token.value;
    }
    return '';
}

function setFormActionMode(mode, form = getDestinationManagementForm()) {
    if (form) {
        form.dataset.mode = mode;
    }
}

function setDestinationManagementModalTitle(title) {
    document.querySelector(SELECTORS.editCreateDestinationModal + ' .modal-title').textContent = title;
}

function clearDestinationForm() {
    const form = getDestinationManagementForm();
    form.reset();
    form.classList.remove(DATA.bootstrapFormValidated);
}