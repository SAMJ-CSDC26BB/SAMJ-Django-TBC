document.addEventListener('DOMContentLoaded', function() {
    initializeDataTable();
    addEventListenersOnEditButtonClick();
    addEventListenersOnSaveButtonClick();
});

function addEventListenersOnEditButtonClick() {
    document.querySelectorAll('.edit-user-btn').forEach(button => {
        button.addEventListener('click', function() {
            let row = this.closest('tr'),
                form = document.querySelector('#userForm');

            if (!form || !row) {
                return;
            }

            let userNameInput = form.querySelector('#username');
            userNameInput.value = row.dataset.username;
            userNameInput.disabled = true;

            form.querySelector('#fullname').value = row.dataset.fullname;
            form.querySelector('#number').value = row.dataset.number;
            form.querySelector('#status').value = row.dataset.status;
            form.querySelector('#role').value = row.dataset.role;
            form.querySelector('#password').value = '';
        });
    });
}

function addEventListenersOnSaveButtonClick() {
    let saveButton = document.querySelector('#editCreateUserModal #saveUserBtn');
    if (!saveButton) {
        return;
    }

    saveButton.addEventListener('click', function() {
        document.querySelector('#userForm').submit();
    });
}

function initializeDataTable() {
    let userTable = document.querySelector('#userTable');
    if (!userTable) {
        return;
    }

    let dataTable = new DataTable(userTable, {
        sortable: true,
        searchable: true,
        fixedHeight: true,
        perPage: 10,
        perPageSelect: [5, 10, 15, 20]
    });
}