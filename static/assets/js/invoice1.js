$(document).ready(function() {
    // Initialize select2


    // Show the buttons when the page is loaded
    $('.customer-buttons-container').show();


    // Event handler for the "Use Random Customer" button
    $('#random-customer-button').on('click', function(event) {
      $('.customer-button').hide();
      event.preventDefault();

      // Generate random customer details
      var randomName = generateRandomName();
      var randomNumber = generateRandomNumber();

      // Check if name and phone are not empty
      if (randomName !== '' && randomNumber !== '') {
        // Save the new customer
        $.ajax({
          url: '/sales/api/customers',
          type: 'POST',
          dataType: 'json',
          data: JSON.stringify({ name: randomName, phone: randomNumber, searchable: 0}),
          contentType: 'application/json',
          success: function(data) {
            // Retrieve the customer ID
            $.ajax({
              url: '/sales/api/customers/' + encodeURIComponent(randomName),
              type: 'GET',
              dataType: 'json',
              success: function(customer) {
        CustomerID = customer.id; // Set the customer ID to the global variable
      }
    });

            newCustomerName = randomName;

            $('#search-input').val(newCustomerName);
            var $select2 = $('#search-input').data('select2');
            $select2.trigger('query', { term: newCustomerName });
            $select2.trigger('open');
            var selectedData = { id: newCustomerName, text: newCustomerName };
            $select2.trigger('select', { data: selectedData });
          }
        });
      }
    });

    // Event handler for the "Search or Add" button
    $('#search-add-button').on('click', function() {
      // Hide both buttons
      $('.customer-button').hide();

      // Show the customer form and clear any existing customer details
      $('.customer-details form').show();
      $('#customer-name, #customer-address, #customer-phone, #customer-debt').text('');
    });
        function generateRandomName() {
      var randomNumber = Math.floor(Math.random() * 90000000) + 10000000; // Generate a random 8-digit number
      var randomName = 'Customer' + randomNumber;
      return randomName;
      }

  // Function to generate a random 11-digit number
    function generateRandomNumber() {
    var randomNumber = Math.floor(Math.random() * 90000000000) + 10000000000;
    return String(randomNumber);
  }



    var newCustomerName = '';
    $('#search-input').select2({
      ajax: {
          url: '/sales/api/customers',
          dataType: 'json',
          delay: 250,
          data: function(params) {
            return {
              term: params.term
            };
          },
          processResults: function(data) {
            // Add the new customer to the list of selectable customers
            if (newCustomerName) {
              data.push({ name: newCustomerName });
            }
            return {
              results: $.map(data, function(item) {
                return {
                  text: item.name,
                  id: item.id
                };
              })
            };
          },
          cache: true
        },
        minimumInputLength: 1,
        placeholder: 'Search for a customer or enter new name and phone number...',
        // Allow manually entered text
        tags: true
    });
var CustomerID; // Declare the global variable
    // Display the customer address and phone on selecting a customer
    $('#search-input').on('select2:select', function (event) {
        var selectedValue = event.params.data.text;
        // Make an AJAX call to fetch the customer details from the server
        $.ajax({
            url: '/sales/api/customers/' + encodeURIComponent(selectedValue),
            type: 'GET',
            dataType: 'json',
            success: function (customer) {

                CustomerID = customer.id; // Set the customer ID to the global variable
                console.log(CustomerID)
                var customerNameElement = $('#customer-name');
                var customerAddressElement = $('#customer-address');
                var customerPhoneElement = $('#customer-phone');
                var customerDebtElement = $('#customer-debt');

                customerNameElement.text('Name: ' + customer.name);
                customerAddressElement.text('Address: ' + customer.address);
                customerPhoneElement.text('Phone: ' + customer.phone);
                customerDebtElement.text('Debt: ' + customer.debt);


                $('.customer-details form, #search-input').hide();
            }
        });
    });

    // Handle form submission
    $('#customer-form').on('submit', function(event) {
        event.preventDefault();
        var name = $('#search-input').val().trim();
        var phone = $('#customer-phone-input').val().trim();
        // Check if name and phone are not empty
        if (name !== '' && phone !== '') {
            // Make an AJAX call to check if customer exists
            $.ajax({
                url: '/sales/api/customers/check',
                type: 'POST',
                dataType: 'json',
                data: JSON.stringify({name: name, phone: phone}),
                contentType: 'application/json',
                success: function (data) {
                    if (data.exists) {
                        // Customer already exists
                        alert('Customer already exists!');
                    } else {
                        // Save the new customer
                        $.ajax({
                            url: '/sales/api/customers',
                            type: 'POST',
                            dataType: 'json',
                            data: JSON.stringify({name: name, phone: phone}),
                            contentType: 'application/json',
                            success: function (data) {
                                alert('Customer saved!');
                                newCustomerName = name;
                $('#search-input').val(newCustomerName);
                var $select2 = $('#search-input').data('select2');
                $select2.trigger('query', { term: newCustomerName });
                $select2.trigger('open');
                var selectedData = { id: newCustomerName, text: newCustomerName };
                $select2.trigger('select', { data: selectedData });

                            }
                        });
                    }

                }
            });
        } else {
            alert('Please enter customer name and phone number!');
        }
    });
    $(document).ready(function() {
      var isPercentageDiscount = true;


//the product section
      // Add product button click event
      $(document).on('click', '#add-product-btn', function() {
        addProductRow();
      });

      // Discount toggle click event
      $(document).on('click', '#discount-toggle', function() {
        isPercentageDiscount = !isPercentageDiscount;

        if (isPercentageDiscount) {
          $(this).text('Discount by %');
          $(this).siblings('.discount').attr('placeholder', 'Discount %');
        } else {
          $(this).text('Flat Discount');
          $(this).siblings('.discount').attr('placeholder', 'Discount');
        }
        $('tbody tr').each(function() {
              calculateProductPrice($(this));
            })
        calculateAllProductPrices();

      });

      // Search input keyup event
      $(document).on('input', '.search-input', function() {
        var searchQuery = $(this).val().toLowerCase();
        var searchResults = $(this).siblings('.search-results');

        // Clear previous results
        searchResults.empty();

        // Send AJAX request to search route
        $.ajax({
          url: '/sales/api/products',
          type: 'GET',
          dataType: 'json',
          success: function(data) {
            // Filter products based on search query
            var filteredProducts = data.filter(function(product) {
              var name = (product.Name1 + ' ' + product.Name2 + ' ' + product.Name3 + ' ' + product.Name4).toLowerCase();
              return name.includes(searchQuery);
            });

            // Display search results
            filteredProducts.forEach(function(product) {
              var listItem = $('<li>').text(product.Name1 + ' - ' + product.Name2 + ' - ' + product.Name3 + ' - ' + product.Name4);
              searchResults.append(listItem);
            });
          }
        });
      });

      // Search result click event
      $(document).on('click', '.search-results li', function() {
        var selectedProduct = $(this).text();
        var productRow = $(this).closest('tr');

        productRow.find('.search-input').val(selectedProduct);
        productRow.find('.search-results').empty();

        getProductPrice(selectedProduct, productRow);
      });

      // Quantity input change event
      $(document).on('input', '.quantity-input', function() {
        var productRow = $(this).closest('tr');
        calculateProductPrice(productRow);
        calculateAllProductPrices();
      });

      // Discount input change event
      $(document).on('input', '.discount', function() {
        var productRow = $(this).closest('tr');
        calculateProductPrice(productRow);
        calculateAllProductPrices();
      });

      function addProductRow() {
        var productRow = $('#product-row').clone();
        productRow.removeAttr('id');
        productRow.find('.search-input').val('');
        productRow.find('.quantity-input').val('1');
        productRow.find('.product-price').text('');
        productRow.find('.discount').val('');
        productRow.find('.total-price').text('');
        productRow.appendTo('tbody');
      }

      function getProductPrice(selectedProduct, productRow) {
        // Retrieve the product price from the API based on the selected product
        // Make an AJAX request to the API to fetch the product price
        $.ajax({
          url: '/sales/api/products',
          type: 'GET',
          dataType: 'json',
          success: function(data) {

            // Find the selected product in the response data
            var selectedProductData = data.find(function(product) {
              return product.Name1 + ' - ' + product.Name2 + ' - ' + product.Name3 + ' - ' + product.Name4 === selectedProduct;
            });

            if (selectedProductData) {
              var productId = selectedProductData.id;
              var productPrice = selectedProductData.retailprice;
              productRow.find('.product-price').text(productPrice);
              productRow.data('productId', productId);
              calculateProductPrice(productRow);
              calculateAllProductPrices();
              console.log('damn success')

              // Send product ID to availability API
              var productId = selectedProductData.id;
              console.log(productId)
              checkProductAvailability(productId,productRow);

            } else {
              // Handle the case when the selected product is not found
              // You can display an error message or perform any other appropriate action
              console.log('Selected product not found');
            }
          },
          error: function() {
            // Handle the error case when the API request fails
            // You can display an error message or perform any other appropriate action
            console.log('Failed to fetch product data');
          }
        });
      }

function checkProductAvailability(productId,productRow) {
  // Make an AJAX request to the availability API with the product ID
  $.ajax({
    url: '/sales/api/check_availability',
    type: 'POST',
    dataType: 'json',
    data: JSON.stringify({ productId: productId }),

    contentType: 'application/json',
    success: function(response) {

      // Handle the availability response data
      // You can update the UI to display the availability status or perform any other appropriate action
      console.log('Response:', response);
   if (response.status === 'success') {
       console.log('Product is available');


       console.log('Quantity in Location 1:', response.quantity);
   } else if (response.status === 'otherlocation') {
     clearProductEntryField(productRow); // Call a function to clear the product entry field
     console.log('Product is not available in shop but we have ' + response.quantity + ' available in other locations please move them before adding');
     alert('Product is not available in shop but we have ' + response.quantity + ' available in other locations please move them before adding');

     calculateAllProductPrices();
   }
 },

  });
    console.log('Product ID:', productId ,productRow);
  }// Console log the product ID

  function clearProductEntryField(productRow) {
    productRow.find('.search-input').val('');
    productRow.find('.product-price').text('');
    productRow.find('.quantity-input').val('1');
    productRow.find('.discount').val('');
    productRow.find('.total-price').text('');
  }



      function calculateProductPrice(productRow) {
        var quantity = parseInt(productRow.find('.quantity-input').val());
        var productPrice = parseFloat(productRow.find('.product-price').text());
        var discountValue = parseFloat(productRow.find('.discount').val());


        if (isNaN(discountValue) || discountValue === '') {
          var totalPrice = productPrice * quantity;
        } else {
          if (isPercentageDiscount) {
            var discountedPrice = productPrice - (productPrice * discountValue / 100);
            var totalPrice = quantity * discountedPrice;
          } else {
            var discountedPrice = productPrice - discountValue;
            var totalPrice = quantity * discountedPrice;
          }
        }

        productRow.find('.total-price').text(totalPrice.toFixed(2));
      }

      function calculateAllProductPrices(productRow) {
        var subtotal = 0;

        $('tbody tr').each(function() {
          var total = parseFloat($(this).find('.total-price').text());
          var isProductAvailable = $(this).data('available');

          if (!isNaN(total) ) {
            console.log(isProductAvailable)
            subtotal += total;
          }

        });

        $('#subtotal-price').text(subtotal.toFixed(2));
        // Calculate and display tax and grand total based on your logic
        // Replace the example calculations with your actual calculations
        var tax = subtotal * 0.0;
        var grandTotal = subtotal + tax;

        $('#tax-price').text(tax.toFixed(2));
        $('#grand-total-price').text(grandTotal.toFixed(2));
      }
    });
//end of product details
//give invoice Number
function getLastInvoiceNumber() {
  fetch('/sales/api/last_invoice_number')
    .then(response => response.json())
    .then(data => {
      // Check if the last_invoice_number exists in the response
      if (data.last_invoice_number !== null) {
        // Increment the last invoice number by 1
        var nextInvoiceNumber = data.last_invoice_number + 1;
        sendInvoiceNumber(nextInvoiceNumber);
      } else {
        // Set a default starting invoice number
        var defaultInvoiceNumber = 1; // Change this to your desired starting number
        sendInvoiceNumber(defaultInvoiceNumber);

      }
    })
    .catch(error => {
      // Handle the error case
      console.error('Error:', error);
    });
}

function sendInvoiceNumber(invoiceNumber) {
  // Send the invoice number to the API for availability check
  fetch('/sales/api/last_invoice_number', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      order_id: invoiceNumber
    })
  })
  .then(response => response.json())
  .then(data => {
    // Check if the invoice number is available or if a suggestion is provided
    if (data.message === 'Number taken') {
      // Use the suggested number
      var suggestion = data.suggestion;
      console.log('Suggested invoice number:', suggestion);
      // Handle the case where the suggested number is already taken as well
      // Update the invoice number on the frontend
      document.getElementById('invoice-number').textContent = 'Invoice #: ' + suggestion;
    } else if (data.message === 'Number available') {
      console.log('Invoice number available:', invoiceNumber);
      // Update the invoice number on the frontend
      document.getElementById('invoice-number').textContent = 'Invoice #: ' + invoiceNumber
      // Handle the case where the selected invoice number is available
    }
  })
  .catch(error => {
    // Handle the error case
    console.error('Error:', error);
  });
}
// Call the function to fetch the last invoice number on page load
getLastInvoiceNumber();

//adding a new invoice tab function
$(document).on('click', '#other-invoice-btn', function() {
  // Open a new window or tab with the desired URL
  var url = 'http://127.0.0.1:5000/sales/invoice'; // Replace with the URL of your new invoice page
  window.open(url, '_blank');
});
// now capturing all the data entered inorder to send it back to datbase
$(document).on('click', '#pay', function() {
  // Get the customer ID
  var customerID = CustomerID;

  // Initialize an array to store product data
  var products = [];

  // Iterate through each product row
  $('tbody tr').each(function() {
    var productRow = $(this);
    var productID = productRow.data('productId');
    var quantity = parseInt(productRow.find('.quantity-input').val());
    var discount = parseFloat(productRow.find('.discount').val());
    // Get the total amount


    // Create an object with product details and add it to the products array
    var product = {
      productID: productID,
      quantity: quantity,
      discount: discount
    };
    products.push(product);
  });

    var totalAmount = parseFloat($('#grand-total-price').text());
  // Create the JSON object
var jsonData = {

  customerID: customerID,
  salesmanID: 1, // Replace with the actual salesman ID
  total_amount: totalAmount,
  items: products
};

  // Log the captured data to the console
  console.log('Customer ID:', customerID);
  console.log('Products:', products);
  console.log('Total Amount:', totalAmount);
  $.ajax({
    url: '/sales/api/sales',
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(jsonData),
    success: function(response) {
      // Handle the success response from the server
      console.log('Sale created successfully');
      // Redirect to the new invoice page
      window.location.href = 'http://127.0.0.1:5000/sales/invoice'; // Replace with the URL of your new invoice page
    },
    error: function(error) {
      // Handle the error response from the server
      console.error('Error:', error);
    }
  });
  // Perform further actions with the captured data (e.g., send it to the server for processing)
});

});
