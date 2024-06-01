document.addEventListener('DOMContentLoaded', function() {
    console.log("Welcome to timeDate page");
});

window.onload = function ()
{
    const timeElement = document.querySelector("#time");
    const dayElement = document.querySelector("#day");
    const dateElement = document.querySelector("#date");

    function fetchTimeDate() {
        fetch('/time_date/')
            .then(response => response.json())
            .then(data => {
                timeElement.textContent = data.time;
                dayElement.textContent = data.day;
                dateElement.textContent = data.date;
            });
    }
    
    setInterval(fetchTimeDate, 1000);

    document.querySelector("body").append("Success -> Status ");
}