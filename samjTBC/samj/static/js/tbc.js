
document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-entry');
    const formPlaceholder = document.getElementById('form-placeholder');

    console.log('DOM fully loaded and parsed');

    if (addButton) {
        console.log('Add button found');
        addButton.addEventListener('click', function() {
            console.log('Add button clicked');
            // Retrieve CSRF token from the hidden input field
            const csrfToken = document.getElementById('csrf-token').value;

            // Use the retrieved CSRF token in the form HTML
            const formHtml = `
                <td></td> <!-- Empty cell for the add/delete button column -->
                <td>
                    <select name="kopfnummer" class="form-control">
                        <option value="4327">4327</option>
                        <option value="4328">4328</option>
                    </select>
                </td>
                <td><input type="text" name="durchwahl" placeholder="Durchwahl" class="form-control"></td>
                <td>
                    <select name="zielnummer" class="form-control">
                        <option value="Beierl">Beierl</option>
                        <option value="Info">Info</option>
                    </select>
                </td>
                <td><input type="datetime-local" name="anfangsdatum" class="form-control"></td>
                <td><input type="datetime-local" name="endedatum" class="form-control"></td>
                <td></td> <!-- Empty cell for the duration column -->
                <td>
                    <button type="submit" class="btn btn-success">Save</button>
                </td>
            `;

            formPlaceholder.innerHTML = `<form method="post" id="entry-form">${formHtml}<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}"></form>`;
            formPlaceholder.style.display = 'table-row';
        });
    } else {
        console.log('Add button not found');
    }
});