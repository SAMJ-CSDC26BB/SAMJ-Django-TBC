document.addEventListener('DOMContentLoaded', function() {
    initializeDataTable();
});

function initializeDataTable() {
    let userTable = document.querySelector('#userTable');
    let dataTable = new DataTable(userTable, {
        sortable: true,
        searchable: true,
        fixedHeight: true,
        perPage: 10,
        perPageSelect: [5, 10, 15, 20]
    });
}