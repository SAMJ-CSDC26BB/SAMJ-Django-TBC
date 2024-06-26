import {ToastBuilder} from '../builder/builder.js';

const DATA_TABLE_DEFAULT_OPTIONS = {
    sortable: true,
    searchable: true,
    fixedHeight: true,
    perPage: 10,
    perPageSelect: [5, 10, 15, 20]
};

/**
 * Function used to initialize a table using Vanilla Datatables.
 * @param tableSelector - table selector (id or class)
 * @param options - options to be used for the table. This is a default param.
 * If not passed, DATA_TABLE_DEFAULT_OPTIONS will be used.
 */
export function initializeVanillaDataTable(tableSelector, options = DATA_TABLE_DEFAULT_OPTIONS) {
    let table = document.querySelector(tableSelector);

    if (!table || typeof DataTable === 'undefined') {
        console.error('Table element or DataTable library not found.');
        return;
    }

    new DataTable(table, options);
}

/**
 * Use bootstrap toast to show notification message.
 * @param message message to be shown
 * @param type type can be success, error, warning, info
 */
export function showNotificationMessage(message, type="success") {
    const myToast = new ToastBuilder();
    myToast.setBody(message);
    myToast.setType(type);
    myToast.show();
}

export function resetForm(form) {
    form.reset();
    form.classList.remove('was-validated');
}

/**
 * Loop through the form elements and add or remove the required attribute.
 * @param form form selector
 * @param isMakeInputsRequired if true, make the inputs required
 */
export function toggleRequiredInputsInForm(form, isMakeInputsRequired) {
    const elements = form.elements;

    for (let i = 0; i < elements.length; i++) {
        const element = elements[i];
        element.required = isMakeInputsRequired;
    }
}

export function closeModal(modalSelector) {
    const modalElement = document.querySelector(modalSelector);
    const modalInstance = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
    if (modalInstance) {
        modalInstance.hide();
    }
}

export function getPropertyFromDataset(node, property) {
    if (!node) {
        return "";
    }

    return node.dataset[property];
}

export function getXMLDocFromString(str) {
    const parser = new DOMParser();
    return parser.parseFromString(str, "text/xml");
}

export function isEmptyObject(obj) {
    return Object.keys(obj).length === 0;
}

export function showMessagesOnDomLoad(messageSelector) {
    let message = document.querySelector(messageSelector);
    if (!message) {
        return;
    }
    if (message.innerText.includes("Login successful")) { // work around
        return;
    }
    if (message) {
        let messageType = message.classList.contains("error") ? "error" : "success";
        showNotificationMessage(message.innerText, messageType);
        message.remove();
    }
}