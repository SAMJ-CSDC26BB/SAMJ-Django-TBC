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
