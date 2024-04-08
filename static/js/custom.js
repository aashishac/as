
function submit_message(message) {
        $.post( "/send_message", {message: message}, handle_response);

    }

$('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        submit_message(input_message)
});

document.getElementById("add-to-cart").addEventListener("click", function(event) {
  event.preventDefault(); // Prevent the default form submission

  // Send an AJAX request to the backend to check login status
  fetch("/api/check_login")
    .then(response => {
      if (response.ok) {
        // User is logged in, proceed with adding to cart
        // You can add the code to add the item to the cart here
        console.log("User is logged in");
      } else {
        // User is not logged in, show a prompt to login
        console.log("User is not logged in");
        alert("Please login to add to cart.");
      }
    })
    .catch(error => console.log(error));
});

