document.addEventListener("DOMContentLoaded", function () {
    // Select the form element
    var form = document.getElementById("locationForm");

    // Add a submit event listener to the form
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      // Create an array to store location data
      var locations = [];

      // Loop through the input fields
      for (var i = 1; i <= 5; i++) {
        var inputField = document.getElementById("LocationName" + i);
        var locationName = inputField.value.trim();

        // Check if the input field is not empty
        if (locationName !== "") {
          locations.push(locationName);
        }
      }

      // Create a JSON object containing the locations
      var data = { locations: locations };

      // Send the JSON data to the server via AJAX (you can implement this part)
      sendDataToServer(data);
    });
  });

  // Function to send data to the server (you need to implement this part)
  function sendDataToServer(data) {
    // Implement your AJAX request here to send 'data' to the server
    // You can use libraries like Axios or the Fetch API for AJAX requests
    // Example using Fetch API:
    fetch("/locations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (response.ok) {
          // Handle a successful response from the server
          console.log("Data sent successfully.");
          // You can redirect or perform other actions here
        } else {
          // Handle errors here
          console.error("Error sending data to the server.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }