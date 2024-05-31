document.addEventListener("DOMContentLoaded", function () {
    const addZielnummer = document.getElementById("addZielnummer");
    const placeholder = document.getElementById("form-placeholder");

    if (addZielnummer) {
        addZielnummer.addEventListener('click', function () {
            const csrfToken = document.getElementById('csrf-token').value;

            // Form HTML with the cancel button
            const formHtml = `
                <form method="post" id="entry-form">
                    <td>
                        <button type="button" class="btn btn-secondary" id="cancel-entry"
                                style="background-color: orange; width: 50px;">C
                        </button>
                    </td>
                    <td><input type="text" name="Zielnummer" placeholder="Zielnummer" class="form-control"></td>
                    <td><input type="text" name="name" placeholder="Name" class="form-control"></td>
                    <td>
                        <button type="submit" class="btn btn-success">Save</button> <!-- Save button -->
                    </td>
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                </form>
            `;

            // Insert the form HTML into the placeholder
            placeholder.innerHTML = formHtml;
            placeholder.style.display = 'table-row';

            // Add event listener for the cancel button
            const cancelButton = document.getElementById('cancel-entry');
            if (cancelButton) {
                cancelButton.addEventListener('click', function () {
                    console.log('Cancel button clicked');
                    placeholder.style.display = 'none'; // Hide the form
                    placeholder.innerHTML = ''; // Clear the form content
                });
            } else {
                console.log('Cancel button not found');
            }
        });
    } else {
        console.log('Add button not found');
    }
});