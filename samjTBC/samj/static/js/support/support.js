/**
 * $(document).ready(function () {
 *     $('form').on('submit', function (event) {
 *         event.preventDefault();  // Prevent the form from being submitted normally
 *         $.ajax({
 *             url: $(this).attr('action'),  // The URL to send the request to
 *             type: $(this).attr('method'),  // The method to use ('get' or 'post')
 *             data: $(this).serialize(),  // The form data
 *             success: function (response) {
 *                 // This function is called if the request succeeds
 *                 // The response parameter contains the data returned by the server
 *                 // You can use this data to update your web page
 *                 console.log(response);
 *             },
 *             error: function (xhr, status, error) {
 *                 // This function is called if the request fails
 *                 console.error('AJAX error:', error);
 *             }
 *         });
 *     });
 * })
 */
