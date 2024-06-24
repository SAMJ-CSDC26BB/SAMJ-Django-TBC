import * as Utils from './utils/utils.js';
import { ButtonBuilder, ElementBuilder } from './builder/builder.js';

const SELECTORS = {
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
    dataTableBottom: '.dataTable-bottom'
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
    populateTbcTable();
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

}
document.querySelectorAll(SELECTORS.saveTbcEntryButton).forEach(button => {
    button.addEventListener('click', onSaveTbcEntryButtonClick)
    });


function onEditTbcEntryButtonClick(event) {
    let row = getTableRowOfEditedTbcEntry(this);
    if (!row) {
        return;
    }

    let tbcForm = getTbcForm();
    if (!tbcForm) {
        return;
    }

    Utils.resetForm(tbcForm);
    Utils.toggleRequiredInputsInForm(tbcForm, false);

    tbcForm.querySelector(SELECTORS.calledNumberInput).value = row.dataset.calledNumber;
    tbcForm.querySelector(SELECTORS.destinationInput).value = row.dataset.destination;
    tbcForm.querySelector(SELECTORS.startDateInput).value = row.dataset.startDate;
    tbcForm.querySelector(SELECTORS.endDateInput).value = row.dataset.endDate;

    setFormActionMode(DATA.editActionMode, tbcForm);
    setTbcEntryModalTitle(DATA.editTbcEntryModalTitle);
}

function onCreateTbcEntryButtonClick(event) {
    let tbcForm = getTbcForm();
    if (!tbcForm) {
        return;
    }

    Utils.resetForm(tbcForm);
    Utils.toggleRequiredInputsInForm(tbcForm, true);
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
    fetch('/api/tbc_management/', {
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
            addTbcEntryToTable(newTbcEntry);
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
    fetch('/api/tbc_management/', {
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
    fetch('/api/tbc_management/', {
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

function addTbcEntryToTable(entry) {
    let tbcTable = document.querySelector(SELECTORS.tbcTable);
    let tableBody = tbcTable.querySelector(SELECTORS.dataTableBody);

    let tableRow = new ElementBuilder('tr')
        .attr({
            'data-id': entry.id,
            'data-called-number': entry.calledNumber,
            'data-destination': entry.destination,
            'data-start-date': entry.startDate,
            'data-end-date': entry.endDate
        })
        .append(new ElementBuilder('td').text(entry.calledNumber))
        .append(new ElementBuilder('td').text(entry.destination))
        .append(new ElementBuilder('td').text(entry.startDate))
        .append(new ElementBuilder('td').text(entry.endDate))
        .append(new ElementBuilder('td')
            .append(new ButtonBuilder('button')
                .class('btn btn-primary btn-sm me-2 edit-tbcEntry-btn')
                .with('data-bs-target', SELECTORS.editCreateTbcEntryModal)
                .with('data-bs-toggle', 'modal')
                .text('Edit'))
            .append(new ButtonBuilder('button')
                .class('btn btn-danger btn-sm delete-tbcEntry-btn')
                .with('data-bs-toggle', 'modal')
                .with('data-bs-target', SELECTORS.deleteTbcEntryModal)
                .text('Delete'))
        );

    tableBody.appendChild(tableRow.element);
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
    return document.querySelector('#tbcEntryForm');  // Update with your actual form ID
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
    return context.closest('tr');
}

function populateTbcTable() {
    fetch('/api/tbc_management/', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Cache-Control': 'max-age=43200' // 12 hours
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (!data.entries) {
                throw new Error("Error fetching TBC entries");
            }

            addTbcEntriesToTable(data.entries);
            Utils.initializeVanillaDataTable(SELECTORS.tbcTable);
            initializeEvents();

        })
        .catch(error => {
            console.error("Error loading TBC entries", error);
            Utils.showNotificationMessage('Error loading TBC entries', "error");
        });
}

function addTbcEntriesToTable(entries) {
    if (!entries) {
        return;
    }

    let tbcTable = document.querySelector(SELECTORS.tbcTable);
    let tableBody = tbcTable.querySelector(SELECTORS.dataTableBody);

    entries.forEach(entry => {
        addTbcEntryToTable(entry);
    });
}

export { populateTbcTable };

