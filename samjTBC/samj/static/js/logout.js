// Show all toast
$(document).ready(function () {
    $('#logout-btn').click(function (e) {
        e.preventDefault();
        $.ajax({
            url: '/logout/',  // Update this to your logout URL
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    // Show toast notification
                    var toastEl = document.querySelector('.toast');
                    var toast = new bootstrap.Toast(toastEl, {autohide: true});
                    toastEl.querySelector('.toast-body').textContent = response.message;
                    toast.show();

                    // Redirect to login page after 2 seconds
                    setTimeout(function () {
                        window.location.href = '/login/';  // Update this to your login URL
                    }, 2000);
                } else {
                    // Show error message
                    alert(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});