// Get the flash message element
var flashMsg = document.getElementById("flash-msg");

// Check if the flash message element exists
if (flashMsg) {
  // Fade out the flash message after 3 seconds
  setTimeout(function() {
    flashMsg.style.opacity = 0;
    setTimeout(function() {
      flashMsg.style.display = "none";
    }, 1000);
  }, 3000);
}
function submitForm() {
  var form = document.getElementById("myForm");
  var inputs = form.querySelectorAll("table tbody td:nth-child(2) input");

  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].value === "") {
      inputs[i].value = "0";
    }
  }

  form.submit();
}
