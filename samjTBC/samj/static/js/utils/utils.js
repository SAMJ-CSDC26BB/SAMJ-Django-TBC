import { ToastBuilder } from '../builder/builder.js';

const dataTableDefaultOptions = {
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
 * If not passed, dataTableDefaultOptions will be used.
 */
export function initializeVanillaDataTable(tableSelector, options = dataTableDefaultOptions) {
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
