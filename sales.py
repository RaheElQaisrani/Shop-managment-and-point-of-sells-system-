from flask import Blueprint, render_template, request, redirect, url_for,flash, jsonify
from datetime import datetime
from model import db, customers,Business, Products, Sales, sales_Items,user,quantity,locations

sales = Blueprint('sales', __name__, url_prefix='/sales')





@sales.route('/customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        cnic = request.form['cnic']
        debit = float(request.form['debit'])
        credit = float(request.form['credit'])
        reference = request.form['reference']
        detail = request.form['detail']
        date_created = datetime.now()
        YAS=1
                # check if customer already exists
        existing_customer = customers.query.filter_by(CNICnumber=cnic).first()
        if existing_customer:
            print (existing_customer)
            flash ('this CNIC is already registerd')
            return redirect(url_for('sales.add_customer'))

        new_customer = customers(name=name, phone=phone, address=address, CNICnumber=cnic,
                                date_created=date_created, debit=debit, credit=credit,
                                reference=reference, detail=detail,debt_allowed=YAS)

        db.session.add(new_customer)
        db.session.commit()
        flash ('customer added sussssfully')

        return redirect(url_for('sales.add_customer'))

    return render_template('add_customer.html')

@sales.route('/invoice')
def one():
    Business1 = Business.query.first()

    return render_template("invoice.html",Business=Business1)

@sales.route('/api/customers')
def get_customers():
    search_term = request.args.get('term', '')
    customers1 = customers.query.filter(customers.name.ilike(f'%{search_term}%'),customers.searchable==1).all()

    results = [{'id':customer.id,'name': customer.name, 'phone': customer.phone} for customer in customers1]

    return jsonify(results)


@sales.route('/api/customers/check', methods=['POST'])
def check_customer():
    data = request.json
    customer = customers.query.filter_by(name=data['name'], phone=data['phone']).first()
    if customer:
        return jsonify({'message': 'Customer already exists!'})
    else:
        return jsonify({'message': 'New customer'})

@sales.route('/api/products')
def api_products():
    products = Products.query.all()
    results = [{'id': product.Sno, 'Name1': product.type, 'Name2': product.title, 'Name3': product.title2,'Name4': product.title3,'retailprice': product.retailpr } for product in products]
    return jsonify(results)

@sales.route('/api/customers', methods=['POST'])
def add_customer_api():
    data = request.json
    searchable = data.get('searchable')
    if searchable != False or searchable != 0: # Check if 'searchable' is False or 0
        searchable = True
    print (searchable)
    customer2 = customers(name=data['name'], phone=data['phone'],searchable = searchable)
    db.session.add(customer2)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully!'})



@sales.route('/api/customers/<string:name>')
def get_customer_details(name):
    # Query the database to retrieve the customer details
    customer = customers.query.filter_by(name=name).first()
    if customer is not None:
        if customer.searchable == 0:
            return jsonify({
                'name': 'customer',
                'address': '',
                'phone': '',
                'debt':'',
                'id':customer.id,
                })
        else:
                return jsonify({
                'name': customer.name,
                'address': customer.address,
                'phone': customer.phone,
                'debt': customer.debt_allowed,
                'id':customer.id,
                })
    else:
        # If the customer is not found, return a 404 error
        return jsonify({'error': 'Customer not found'}), 404
# API endpoint to check product availability in location 1
@sales.route('/api/check_availability', methods=['POST'])
def check_availability():
    # Get the product ID from the request
    product_id = request.json['productId']
    print (product_id)
    # checking product at all locations
    # allqty = quantity.query.filter_by(ProductID=product_id).all()
     # Retrieve the quantity and location name for all locations
    result = db.session.query(quantity.Quantity, locations.locationName).join(locations).filter(quantity.ProductID == product_id).all()

    # Create a dictionary to store the quantity for each location
    location_qty = {location_name: qty for qty, location_name in result}
    # calculating all the quantities
    allqty = sum(location_qty.values())
    # Check if the product is available in location 1
    qty = quantity.query.filter_by(ProductID=product_id, LocationID=1).first()
    print (qty)
    print (location_qty)
    print (allqty)
    if qty:
        total_quantity = qty.Quantity
        if total_quantity > 0:
            return jsonify({'status': 'success', 'message': 'Product is available.', 'quantity': total_quantity})
        elif total_quantity < 1 and allqty > 0 :
            return jsonify({'status': 'otherlocation', 'message': 'This product is not available in any location.','quantity': allqty})
    else:
        return jsonify({'status': 'error', 'message': 'Please move product from other locations before adding them.'})

@sales.route('/api/last_invoice_number', methods=['GET', 'POST'])
def get_last_invoice_number():
    if request.method == 'GET':
        last_invoice = Sales.query.order_by(Sales.orderid.desc()).first()
        if last_invoice:
            return jsonify({'last_invoice_number': last_invoice.orderid})
            print(last_invoice.orderid)
        else:
            return jsonify({'last_invoice_number': None})
            # the bellow part is some overengineered stuff

    elif request.method == 'POST':
        data = request.json
        order_id = data.get('order_id')

        if not order_id:
            return jsonify({'message': 'Invalid request. Missing order_id in the request.'}), 400

        # Check if the order ID is available in the database
        existing_order = Sales.query.filter_by(orderid=order_id).first()
        if existing_order:
            # Order ID is already taken, find an available number as a suggestion
            suggestion = find_available_order_id()
            return jsonify({'message': 'Number taken', 'suggestion': suggestion}), 409

        # Order ID is available
        return jsonify({'message': 'Number available'}), 200
def find_available_order_id():
    # Retrieve the last entered order ID from the database
    last_invoice = Sales.query.order_by(Sales.orderid.desc()).first()

    if last_invoice:
        last_order_id = last_invoice.orderid
    else:
        # If there are no existing orders, start with a default value
        last_order_id = 1000

    # Define the maximum number of attempts to find an available order ID
    max_attempts = 100

    # Define the step size to generate suggestions (you can adjust this as needed)
    step_size = 5

    # Start searching for a suggestion
    for attempt in range(max_attempts):
        # Generate the suggested order ID by adding the step size
        suggestion = last_order_id + step_size

        # Check if the suggested order ID is available in the database
        existing_order = Sales.query.filter_by(orderid=suggestion).first()
        if not existing_order:
            # Suggested order ID is available, return it as a suggestion
            return suggestion

        # If the suggestion is not available, try the next nearest order ID
        suggestion = last_order_id - step_size
        if suggestion > 0:
            existing_order = Sales.query.filter_by(orderid=suggestion).first()
            if not existing_order:
                # Suggested order ID is available, return it as a suggestion
                return suggestion

    # If no available order ID is found after max_attempts, return None or raise an exception
    return None
# till here it was not needed but just did it to prevent 0.01 of this ever heppening

@sales.route('/api/sales', methods=['POST'])
def create_sale():
    data = request.json
    # Extract data from the request
    customer_id = data.get('customerID')
    salesman_id = data.get('salesmanID')
    total_amount = data.get('total_amount')
    items = data.get('items')

    # Create a new Sales object
    sale = Sales(customerID=customer_id, salesmanID=salesman_id, total_amount=total_amount)

    # Create SalesItems objects for each item and associate them with the sale
    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity')
        profit = item.get('profit')
        sale_item = sales_Items(product_id=product_id, quantity=quantity, profit=profit)
        db.session.add(sale_item)

    # Save the data to the database
    db.session.add(sale)
    db.session.commit()
    print('all done')
    return jsonify({'message': 'Sale created successfully'})
