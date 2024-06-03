document.addEventListener('DOMContentLoaded', function() {
    console.log("Welcome to timeDate page");
});

window.onload = function ()
{
    const timeElement = document.querySelector("#text");

    function fetchTimeDate(string) {
        fetch('/time_date/')
            .then(response => response.text())
            .then(data => {
                console.log(data);
                timeElement.innerHTML = data;
            });
    }
    
    setInterval(fetchTimeDate, 1000);

    document.querySelector("body").append("Success -> Status ");
}