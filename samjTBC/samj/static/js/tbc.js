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
                <td colspan="8">
                    <form method="post" id="entry-form">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                        <select name="kopfnummer">
                            <option value="4327">4327</option>
                            <option value="4328">4328</option>
                        </select>
                        <input type="text" name="durchwahl" placeholder="Durchwahl">
                        <select name="zielnummer">
                            <option value="Beierl">Beierl</option>
                            <option value="Info">Info</option>
                        </select>
                        <input type="datetime-local" name="anfangsdatum">
                        <input type="datetime-local" name="endedatum">
                        <button type="submit" class="btn btn-success">Save</button>
                    </form>
                </td>
            `;

            formPlaceholder.innerHTML = formHtml;
            formPlaceholder.style.display = 'table-row';
        });
    } else {
        console.log('Add button not found');
    }
});