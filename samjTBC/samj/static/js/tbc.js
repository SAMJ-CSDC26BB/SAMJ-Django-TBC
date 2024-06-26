import * as Utils from './utils/utils.js';
import { ButtonBuilder, ElementBuilder } from './builder/builder.js';




const SELECTORS = {
    // Buttons for Destination Management
    createDestinationButton: '#create-destination-btn',
    saveDestinationButton: '#saveDestinationBtn',
    deleteDestinationButton: '.uiDeleteDestinationButton',
    editDestinationButton: '.edit-destination-btn', // Generated edit button for destinations
    deleteDestinationRowButton: '.delete-destination-btn', // Generated delete button for destinations

    // Modals for Destination Management
    editCreateDestinationModal: '#editCreateDestinationModal',
    deleteDestinationModal: '#deleteDestinationModal',

    // Forms for Destination Management
    destinationForm: '#destinationForm',

    // Form Inputs for Destination Management
    destinationNameInput: '#destinationName',
    destinationNumberInput: '#destination',

    // Tables and Table Body for Destination Management
    destinationsTable: '#destinationsTable',
    destinationTableBody: '.uiDestinationTableBody',

    // Common Selectors (already existing from previous set)
    editTbcEntryButton: '.edit-tbcEntry-btn',
    deleteTbcEntryButton: '.delete-tbcEntry-btn',
    deleteTbcEntryBtnInModal: '.uiDeleteTbcEntryButton',
    modalBodyMessage: '.modal-body-message',
    createTbcEntryButton: '.create-tbcEntry-btn',
    saveTbcEntryButton: '#saveTbcEntryBtn',
    calledNumberInput: '#calledNumber',
    destinationInput: '#destination',
    startDateInput: '#startDate',
    endDateInput: '#endDate',
    tbcTable: '#tbcTable',
    dataTableBody: '.uiTbcBody',
    editCreateTbcEntryModal: '#editCreateTbcEntryModal',
    editCreateTbcEntryModalTitle: '.modal-title',
    deleteTbcEntryModal: '#deleteTbcEntryModal',
    csrfToken: "[name=csrfmiddlewaretoken]",
    dataTableBottom: '.dataTable-bottom',
    callForwardingTable: '#tbcTable',
    callForwardingForm: '#tbcEntryForm',
};


const DATA = {
    editActionMode: 'edit',
    createActionMode: 'create',
    editTbcEntryModalTitle: 'Edit TBC Entry',
    createTbcEntryModalTitle: 'Create TBC Entry',
    bootstrapFormValidated: 'was-validated',
    displayNoneClassName: 'd-none'
};

document.addEventListener('DOMContentLoaded', function () {
    populateCallForwardingTable();
});

function initializeEvents() {
    document.querySelectorAll(SELECTORS.editTbcEntryButton).forEach(button => {
        button.addEventListener('click', onEditTbcEntryButtonClick);
    });

    document.querySelectorAll(SELECTORS.deleteTbcEntryButton).forEach(button => {
        button.addEventListener('click', onDeleteTbcEntryButtonClick);
    });

    document.querySelectorAll(SELECTORS.createTbcEntryButton).forEach(button => {
        button.addEventListener('click', onCreateTbcEntryButtonClick);
    });

    document.querySelectorAll(SELECTORS.saveTbcEntryButton).forEach(button => {
        button.addEventListener('click', onSaveTbcEntryButtonClick)
    });

}


function populateCallForwardingTable() {
    fetch('/api/call_forwarding_management/', {
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
            if (!data.call_forwardings) {
                throw new Error("Error fetching call forwardings");
            }
            addCallForwardingsToTable(data.call_forwardings);
            Utils.initializeVanillaDataTable(SELECTORS.callForwardingTable);
            initializeEvents();

        })
        .catch(error => {
            console.error(error.message)
            Utils.showNotificationMessage('Error loading the Call Forwarding', error.message);
        });
}

function addCallForwardingsToTable(callForwardings) {
    if (!callForwardings) {
        return;
    }

    let callForwardingTable = document.querySelector(SELECTORS.callForwardingTable);
    if (!callForwardingTable) {
        throw new Error("Error fetching call forwardings, no callForwardingTable table found");
    }
    callForwardings.forEach(callForwarding => {
        addCallForwardingToTable(callForwarding);
    });
}

function addCallForwardingToTable(callForwarding) {
    let callForwardingTable = document.querySelector(SELECTORS.callForwardingTable);
    let tableBody = callForwardingTable.querySelector(SELECTORS.dataTableBody);

    // Create Edit button
    let editButton = new ButtonBuilder()
        .class("btn btn-primary btn-sm me-2 edit-tbcEntry-btn")
        .with("data-bs-target", SELECTORS.editCreateTbcEntryModal)
        .with("data-bs-toggle", "modal")
        .text("Edit");

    // Create Delete button
    let deleteButton = new ButtonBuilder("button")
        .class("btn btn-danger btn-sm delete-tbcEntry-btn")
        .with("data-bs-toggle", "modal")
        .with("data-bs-target", SELECTORS.deleteTbcEntryModal)
        .text("Delete");

    // Create table row
    let tableRow = new ElementBuilder("tr")
        .attr({
            'data-called-number': callForwarding.calledNumber__number,
            'data-destination-number': callForwarding.destination__number,
            'data-start-date': callForwarding.startDate,
            'data-end-date': callForwarding.endDate
        })
        .append(new ElementBuilder("td").class("tableDataCalledNumber").text(callForwarding.calledNumber__number))
        .append(new ElementBuilder("td").class("tableDataDestinationNumber").text(callForwarding.destination__number))
        .append(new ElementBuilder("td").class("tableDataStartDate").text(callForwarding.startDate))
        .append(new ElementBuilder("td").class("tableDataEndDate").text(callForwarding.endDate))
        .append(new ElementBuilder("td").class("tableDataActions").append(editButton).append(deleteButton));

    // Append the constructed row to the table body
    tableBody.append(tableRow.element);
}






function onEditTbcEntryButtonClick(event) {
    let button = event.currentTarget;
    let row = button.closest('tr');
    if (!row) {
        console.error("No table row found for the clicked edit button.");
        return;
    }

    let tbcForm = document.getElementById('tbcEntryForm');
    if (!tbcForm) {
        console.error("No form found with ID 'tbcEntryForm'.");
        return;
    }

    // Reset the form and disable required inputs for editing
    tbcForm.reset();
    Utils.toggleRequiredInputsInForm(tbcForm, false);

    // Set the form values based on the table row data
    tbcForm.querySelector(SELECTORS.calledNumberInput).value = row.querySelector('.tableDataCalledNumber').textContent.trim();
    tbcForm.querySelector(SELECTORS.destinationInput).value = row.querySelector('.tableDataDestinationNumber').textContent.trim();
    tbcForm.querySelector(SELECTORS.startDateInput).value = row.querySelector('.tableDataStartDate').textContent.trim();
    tbcForm.querySelector(SELECTORS.endDateInput).value = row.querySelector('.tableDataEndDate').textContent.trim();

    // Update the form action mode and modal title
    setFormActionMode(DATA.editActionMode, tbcForm);
    setTbcEntryModalTitle(DATA.editTbcEntryModalTitle);
}

function onCreateTbcEntryButtonClick(event) {
    let tbcForm = document.getElementById('tbcEntryForm');
    if (!tbcForm) {
        console.error("No form found with ID 'tbcEntryForm'.");
        return;
    }

    // Reset the form and enable required inputs for creating a new entry
    tbcForm.reset();
    fetchTbcEntryData()
    Utils.toggleRequiredInputsInForm(tbcForm, true);

    // Update the form action mode and modal title
    setFormActionMode(DATA.createActionMode, tbcForm);
    setTbcEntryModalTitle(DATA.createTbcEntryModalTitle);
}



function onSaveTbcEntryButtonClick(event) {
    console.log("save button clicked")
    const form = getTbcForm();
    if (!form || !form.dataset.mode) {
        return;
    }

    if (form.dataset.mode === DATA.createActionMode) {
        createTbcEntry(form);
    } else {
        editTbcEntry(form);
    }
}

function createTbcEntry(tbcForm = getTbcForm()) {
    if (!tbcForm || !tbcForm.checkValidity()) {
        tbcForm.classList.add(DATA.bootstrapFormValidated);
        return;
    }

    const newTbcEntry = getTbcEntryDataFromForm(tbcForm);
    createNewTbcEntry(newTbcEntry);
}

function createNewTbcEntry(newTbcEntry) {
    fetch('/api/call_forwarding_management/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
        },
        body: JSON.stringify(newTbcEntry)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            return response.json();
        })
        .then(data => {
            Utils.closeModal(SELECTORS.editCreateTbcEntryModal);
            Utils.showNotificationMessage(`TBC Entry created successfully`);
            addCallForwardingToTable(newTbcEntry);
            initializeEvents();

            let tableBottom = document.querySelector(SELECTORS.dataTableBottom);
            if (tableBottom) {
                tableBottom.style = 'margin-top:50px';
            }

        })
        .catch(error => {
            console.error('Error creating TBC Entry:', error);
            Utils.showNotificationMessage('Error creating TBC Entry', "error");
        });
}

function editTbcEntry(tbcForm = getTbcForm()) {
    if (!tbcForm) {
        return;
    }

    if (!tbcForm.checkValidity()) {
        tbcForm.classList.add(DATA.bootstrapFormValidated);
        return;
    }

    const updatedTbcEntry = getTbcEntryDataFromForm(tbcForm);
    updateTbcEntry(updatedTbcEntry);
}

function updateTbcEntry(updatedTbcEntry) {
    fetch('/api/call_forwarding_management/', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
        },
        body: JSON.stringify(updatedTbcEntry)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            Utils.closeModal(SELECTORS.editCreateTbcEntryModal);
            Utils.showNotificationMessage(`TBC Entry updated successfully`);
            updateTbcEntryInTable(updatedTbcEntry);
        })
        .catch(error => {
            console.error('Error updating TBC Entry:', error);
            Utils.showNotificationMessage('Error updating TBC Entry', "error");
        });
}

function onDeleteTbcEntryButtonClick(event) {
    const row = getTableRowOfEditedTbcEntry(this);
    if (!row) {
        return;
    }

    const deleteTbcEntryModal = document.querySelector(SELECTORS.deleteTbcEntryModal);
    if (deleteTbcEntryModal) {
        deleteTbcEntryModal.querySelector(SELECTORS.modalBodyMessage).innerText
            = deleteTbcEntryModal.querySelector(SELECTORS.modalBodyMessage).innerText.replace('{0}', row.dataset.calledNumber);

        deleteTbcEntryModal.querySelector(SELECTORS.deleteTbcEntryBtnInModal).addEventListener('click', (e) => { deleteTbcEntry(row) });
    }
}

function deleteTbcEntry(row) {
    fetch('/api/call_forwarding_management/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfTokenFromForm()
        },
        body: JSON.stringify({ id: row.dataset.id })
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
            Utils.showNotificationMessage(`TBC Entry deleted successfully`, "success");
            Utils.closeModal(SELECTORS.deleteTbcEntryModal);
            row.remove();
        })
        .catch(error => {
            console.error('Error deleting TBC Entry:', error);
            Utils.showNotificationMessage('Error deleting TBC Entry', "error");
        });
}



function updateTbcEntryInTable(updatedEntry) {
    let tbcTable = document.querySelector(SELECTORS.tbcTable);
    let updatedTbcEntryRow = tbcTable.querySelector(`[data-id='${updatedEntry.id}']`);
    if (!updatedTbcEntryRow) {
        return;
    }
    updatedTbcEntryRow.dataset.calledNumber = updatedEntry.calledNumber;
    updatedTbcEntryRow.dataset.destination = updatedEntry.destination;
    updatedTbcEntryRow.dataset.startDate = updatedEntry.startDate;
    updatedTbcEntryRow.dataset.endDate = updatedEntry.endDate;

    updatedTbcEntryRow.cells[0].innerText = updatedEntry.calledNumber;
    updatedTbcEntryRow.cells[1].innerText = updatedEntry.destination;
    updatedTbcEntryRow.cells[2].innerText = updatedEntry.startDate;
    updatedTbcEntryRow.cells[3].innerText = updatedEntry.endDate;
}

function setTbcEntryModalTitle(title) {
    let modal = document.querySelector(SELECTORS.editCreateTbcEntryModal);
    if (modal) {
        modal.querySelector(SELECTORS.editCreateTbcEntryModalTitle).innerText = title;
    }
}

function getTbcForm() {
    return document.querySelector(SELECTORS.callForwardingForm);  // Update with your actual form ID
}

function setFormActionMode(mode, form = getTbcForm()) {
    if (form) {
        form.dataset.mode = mode;
    }
}

function getTbcEntryDataFromForm(form) {
    return {
        calledNumber: form.querySelector(SELECTORS.calledNumberInput).value,
        destination: form.querySelector(SELECTORS.destinationInput).value,
        startDate: form.querySelector(SELECTORS.startDateInput).value,
        endDate: form.querySelector(SELECTORS.endDateInput).value
    };
}

function getCsrfTokenFromForm(form = getTbcForm()) {
    let token = form.querySelector(SELECTORS.csrfToken);
    if (token) {
        return token.value;
    }
    return '';
}

function getTableRowOfEditedTbcEntry(context) {
    return context.closest(SELECTORS.tableRow);
}




document.querySelector(SELECTORS.createTbcEntryButton).addEventListener('click', function() {
    let callForwadingForm = getTbcForm()
    Utils.resetForm(callForwadingForm);  // Function to reset the form fields
    fetchTbcEntryData(); // Fetch data for the modal
});

function fetchTbcEntryData() {
    fetch('/api/edit_create_tbc_entry/',{
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=1', // 12 hours
        }
    })

        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update dropdowns with fetched data
            console.log(data);

            updateCalledNumberDropdown(data.call_forwardings);
            updateDestinationDropdown(data.call_forwardings);

            // Show the modal after data is loaded
            let modal = new bootstrap.Modal(document.getElementById('editCreateTbcEntryModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching TBC entry data:', error);
            // Handle error scenario
        });
}

function updateCalledNumberDropdown(callForwardings) {
    let calledNumberSelect = document.querySelector(SELECTORS.calledNumberInput);
    calledNumberSelect.innerHTML = '<option value="">Select called number...</option>';  // Clear previous options

    callForwardings.forEach(function(cf) {
        let option = document.createElement('option');
        option.value = cf.calledNumber__number;
        option.textContent = cf.calledNumber__number;
        calledNumberSelect.appendChild(option);
    });
}

function updateDestinationDropdown(callForwardings) {
    let destinationSelect = document.querySelector(SELECTORS.destinationInput);
    destinationSelect.innerHTML = '<option value="">Select destination...</option>';  // Clear previous options

    callForwardings.forEach(function(cf) {
        let option = document.createElement('option');
        option.value = cf.destination__number;
        option.textContent = cf.destination__number;
        destinationSelect.appendChild(option);
    });
}



