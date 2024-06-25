import * as Utils from './utils/utils.js';
import {ButtonBuilder, ElementBuilder} from './builder/builder.js';

const SELECTORS = {
    // Buttons
    createDestinationButton: '.create-destination-btn',
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


function populateDestinationsTable() {
    fetch('/api/destination_management/', {
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
            if (!data.destinations) {
                throw new Error("Error fetching destinations");
            }

            addDestinationsToTable(data.destinations);
            Utils.initializeVanillaDataTable('#destinationsTable');
            initializeEvents()

        })
        .catch(error => {
            Utils.showNotificationMessage('Error loading the Destination', "error");
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
    console.log(destinations);
    destinations.forEach(destination => {
        console.log(destination.number);
        addDestinationToTable(destination);
    });
}

function addDestinationToTable(destination) {
    console.log("addDestinationToTable");
    console.log(destination);
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


function onCreateButtonClick(event) {
    let destinationForm = getDestinationManagementForm();
    if (!destinationForm) {
        return;
    }

    destinationForm.querySelector(SELECTORS.usernameInput).disabled = false;

    Utils.resetForm(destinationForm);
    Utils.toggleRequiredInputsInForm(destinationForm, true);
    setFormActionMode(DATA.createActionMode, destinationForm);
    setUserManagementModalTitle(DATA.createUserModalTitle);
}


function createDestination(destinationData) {
    fetch('/api/destination_management/', {
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
    fetch('/api/destination_management/', {
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