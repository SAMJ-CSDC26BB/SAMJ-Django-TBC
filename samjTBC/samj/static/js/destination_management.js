import * as Utils from './utils/utils.js';
import {ButtonBuilder, ElementBuilder} from "./builder/builder";

document.addEventListener('DOMContentLoaded', () => {
    const SELECTORS = {
        createDestinationButton: '.create-destination-btn',
        saveDestinationButton: '#saveDestinationBtn',
        destinationForm: '#destinationForm',
        destinationTableBody: '.uiDestinationTableBody',
        deleteDestinationModal: '#deleteDestinationModal',
        deleteDestinationButton: '.uiDeleteDestinationButton',
        destinationsTable: '#editCreateDestinationModal'
    };

    document.addEventListener('DOMContentLoaded', function () {
        populateDestinationsTable();
    });

    let currentDestination = null;

    document.querySelectorAll(SELECTORS.createDestinationButton).forEach(button => {
        button.addEventListener('click', () => {
            clearForm();
            currentDestination = null;
        });
    });

    document.querySelector(SELECTORS.saveDestinationButton).addEventListener('click', () => {
        const form = document.querySelector(SELECTORS.destinationForm);
        if (form.checkValidity()) {
            const formData = new FormData(form);
            const destinationData = {
                name: formData.get('name'),
                number: formData.get('number'),
            };
            if (currentDestination) {
                destinationData.number = currentDestination.number;
                updateDestination(destinationData);
            } else {
                createDestination(destinationData);
            }
        }
    });

    document.querySelector(SELECTORS.deleteDestinationButton).addEventListener('click', () => {
        if (currentDestination) {
            deleteDestination(currentDestination);
        }
    });

    fetchDestinations();

    function fetchDestinations() {
        fetch('/api/destination_management/')
            .then(response => response.json())
            .then(data => {
                const destinations = data.number;

                addDestinationToTable(data.number, data.name)


                const tbody = document.querySelector(SELECTORS.destinationTableBody);
                tbody.innerHTML = '';
                destinations.forEach(destination => {
                    const row = createDestinationRow(destination);
                    tbody.appendChild(row);
                });
            });
    }

    function createDestination(destinationData) {
        fetch('/api/destination_management/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(destinationData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    fetchDestinations();
                    closeModal();
                }
            });
    }

    function updateDestination(destinationData) {
        fetch('/api/destination_management/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(destinationData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    fetchDestinations();
                    closeModal();
                }
            });
    }

    function deleteDestination(destinationData) {
        fetch('/api/destination_management/', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({ id: destinationData.id }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    fetchDestinations();
                    closeModal();
                }
            });
    }

    function createDestinationRow(destination) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${destination.name}</td>
            <td>${destination.number}</td>
            <td>
                <button class="btn btn-primary btn-sm edit-btn" data-id="${destination.id}" data-bs-toggle="modal" data-bs-target="#editCreateDestinationModal">Edit</button>
                <button class="btn btn-danger btn-sm delete-btn" data-id="${destination.id}" data-bs-toggle="modal" data-bs-target="#deleteDestinationModal">Delete</button>
            </td>
        `;

        row.querySelector('.edit-btn').addEventListener('click', () => {
            currentDestination = destination;
            fillForm(destination);
        });

        row.querySelector('.delete-btn').addEventListener('click', () => {
            currentDestination = destination;
        });

        return row;
    }

    function fillForm(destination) {
        const form = document.querySelector(SELECTORS.destinationForm);
        form.querySelector('#destinationName').value = destination.name;
        form.querySelector('#destinationNumber').value = destination.number;
    }

    function clearForm() {
        const form = document.querySelector(SELECTORS.destinationForm);
        form.reset();
    }

    function closeModal() {
        const modal = bootstrap.Modal.getInstance(document.querySelector('.modal.show'));
        if (modal) {
            modal.hide();
        }
    }

    // test coppied funcitions

    function addDestinationsToTable(destinations) {
        if (!destinations) {
            return;
        }

        let destinationsTable = document.querySelector(SELECTORS.destinationsTable);
        if (!destinationsTable) {
            throw new Error("Error fetching destinations, no user table found");
        }
        destinations.forEach(destination => {
            addDestinationToTable(destination);
        });
    }

    function addDestinationToTable(number, name) {
        let destinationsTable = document.querySelector(SELECTORS.destinationsTable);
        let tableBody = destinationsTable.querySelector(SELECTORS.tableBody);

        // Create Edit button
        let editButton = new ButtonBuilder()
            .class("btn btn-primary btn-sm me-2 edit-destination-btn")
            .with("data-bs-target", SELECTORS.destinationsTable)
            .with("data-bs-toggle", "modal")
            .text("Edit");

        // Create Delete button
        let deleteButton = new ButtonBuilder("button")
            .class("btn btn-danger btn-sm delete-destination-btn")
            .with("data-bs-toggle", "modal")
            .with("data-bs-target", SELECTORS.deleteDestinationModal)
            .text("Delete");

        // Create table row
        let tableRow = new ElementBuilder("tr")
            .attr({
                'Destination Number': number,
                'Name': name
            })
            .append(new ElementBuilder("td").class("tableDataNumber").text(number))
            .append(new ElementBuilder("td").class("tableDataName").text(name))
            .append(new ElementBuilder("td").class("tableDataActions").append(editButton).append(deleteButton));

        // Append the constructed row to the table body
        tableBody.append(tableRow.element);
    }


    function populateDestinationsTable() {
        fetch('/api/destination_management/', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Cache-Control': 'max-age=43200', // 12 hours
            }
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                if (!data.destination) {
                    throw new Error("Error fetching destinations");
                }

                addDestinationsToTable(data.destination);
                Utils.initializeVanillaDataTable('#destinationsTable');

            })
            .catch(error => {
                console.log("Error loading users", error);
                Utils.showNotificationMessage('Error loading the users', "error");
            });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
