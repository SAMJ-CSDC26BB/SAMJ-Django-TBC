document.addEventListener("DOMContentLoaded", function () {
    const ticketContainer = document.getElementById('ticketContainer');
    const stateFilter = document.getElementById('stateFilter');
    const creationDate = document.getElementById('creationDate'); // Changed from startDate
    const keywordSearch = document.getElementById('keywordSearch');

    const filterTickets = () => {
        const state = stateFilter.value;
        const created = creationDate.value ? new Date(creationDate.value) : null; // Changed from start
        const keyword = keywordSearch.value.toLowerCase();

        const tickets = document.querySelectorAll('.ticket');
        tickets.forEach(ticket => {
            const ticketState = ticket.dataset.state;
            const ticketCreated = new Date(ticket.dataset.created);
            const ticketText = ticket.innerText.toLowerCase();

            let stateMatch = (state === 'all') || (ticketState === state);
            let dateMatch = (!created || ticketCreated >= created); // Changed from start
            let keywordMatch = !keyword || ticketText.includes(keyword);

            if (stateMatch && dateMatch && keywordMatch) {
                ticket.style.display = 'block';
            } else {
                ticket.style.display = 'none';
            }
        });
    };

    stateFilter.addEventListener('change', filterTickets);
    creationDate.addEventListener('input', filterTickets); // Changed from startDate
    keywordSearch.addEventListener('input', filterTickets);

    // Initial filter to show only open tickets
    filterTickets();

    const bodies = document.querySelectorAll('pre.card-text.bg-light.p-3.rounded');

    bodies.forEach(body => {
        // Remove 'yaml' and triple backticks from the text
        let cleanedText = body.innerHTML.replace(/```yaml\s*|```/g, '');
        if (cleanedText.length > 300) {
            const shortText = cleanedText.slice(0, 300) + '...';
            const fullText = cleanedText;
            body.innerHTML = shortText;

            const showMoreBtn = document.createElement('button');
            showMoreBtn.className = 'btn btn-link p-0';
            showMoreBtn.innerHTML = 'Show more';
            body.parentNode.appendChild(showMoreBtn);

            showMoreBtn.addEventListener('click', function () {
                if (body.innerHTML === shortText) {
                    body.innerHTML = fullText;
                    showMoreBtn.innerHTML = 'Show less';
                } else {
                    body.innerHTML = shortText;
                    showMoreBtn.innerHTML = 'Show more';
                }
            });
        } else {
            body.innerHTML = cleanedText;
        }
    });
});