from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from sqlalchemy import or_
from flask_migrate import Migrate






app = Flask(__name__)
app.secret_key = "Rahe3l"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://raheel:Rahe3l.11@localhost/stock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
from model import model,db, Products,locations,quantity,user
from sales import sales
app.register_blueprint(sales)

db.init_app(app)
migrate = Migrate(app, db)
# db.init_app(app)
# db =SQLAlchemy(app)
#
#
# class Products(db.Model):
#      __tablename__ = "Products"
#      Sno = db.Column(db.Integer, primary_key=True)
#      type=db.Column(db.String(255), nullable=False)
#      title=db.Column(db.String(255), nullable=True)
#      title2=db.Column(db.String(255), nullable=True)
#      title3=db.Column(db.String(255), nullable=True)
#      purchesepr=db.Column(db.Integer)
#      retailpr=db.Column(db.Integer)
#      wholepr=db.Column(db.Integer)
#
# class locations(db.Model):
#      __tablename__ = "locations"
#      LocationID = db.Column(db.Integer,primary_key=True)
#      locationName =db.Column(db.String(255),nullable=True)
#
#
# class quantity(db.Model):
#      __tablename__ = "quantity"
#      QID = db.Column(db.Integer,primary_key=True)
#      LocationID=db.Column(db.Integer,db.ForeignKey('locations.LocationID'))
#      ProductID=db.Column(db.Integer,db.ForeignKey('Products.Sno'))
#      Quantity=db.Column(db.Integer)
#
# class user(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     Password = db.Column(db.String(255))
#     phoneno = db.Column(db.String(25))
#     is_superuser = db.Column(db.Boolean, default=False)
#
# class customers(db.Model):
#     __tablename__ = "customer"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     address = db.Column(db.String(255))
#     cnic_number = db.Column(db.String(15))
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)
#     debit = db.Column(db.Float)
#     credit = db.Column(db.Float)
#     reference = db.Column(db.String(255))
#     detail = db.Column(db.String(255))



@app.route('/', methods=["POST", "GET"])
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Get the product to be updated
    else:
        loc = locations.query.all()
        if request.method == "POST":
            Type = request.form["Type"]
            title = request.form["title"]
            title2 = request.form["title2"]
            title3 = request.form["title3"]
            purchesepr = request.form["purchesepr"]
            retailpr = request.form["retailpr"]
            wholepr = request.form["wholepr"]
            # LocationID = request.form["LocationID"]
            if request.method == "POST":
                # Add product to Products table
                product = Products(type=Type, title=title, title2=title2, title3=title3, purchesepr=purchesepr,
                                   retailpr=retailpr, wholepr=wholepr,)
                db.session.add(product)
                db.session.commit()

                # Add product quantity to Quantity table for each location
                for loc in locations.query.all():
                    qty = request.form[f"qty_{loc.LocationID}"]
                    print(qty)
                    product_qty = quantity(LocationID=loc.LocationID, ProductID=product.Sno, Quantity=qty)
                    db.session.add(product_qty)
                    db.session.commit()

                flash('Product added successfully!', 'success')
                return redirect(url_for("home"))
            else:
                user = session['user']
                return render_template("data.html", user=user, loc=loc)
        elif "user" in session:
            user = session['user']
            return render_template("data.html", user=user, loc=loc)
        else:
            return redirect(url_for("login"))



@app.route('/search')
def search():
    search_term = request.args.get('term', '')
    products = db.session.query(Products).filter(or_(Products.title.ilike(f'%{search_term}%'),
                                                      Products.type.ilike(f'%{search_term}%'),
                                                      Products.title2.ilike(f'%{search_term}%'),
                                                      Products.title3.ilike(f'%{search_term}%'))).all()
    results = [{'id': product.Sno, 'Price': product.retailpr, 'text': f'{product.type} - {product.title} - {product.title2} - {product.title3}'} for product in products]
    print (results)
    return jsonify(results)

@app.route('/search1')
def search1():
    if 'user' not in session:
        return redirect(url_for('login'))
    # Get the product to be updated
    else:
        return render_template('search.html')



@app.route('/update/<int:Sno>', methods=["GET", "POST"])
def update(Sno):
    if 'user' not in session:
        return redirect(url_for('login'))
    # Get the product to be updated
    else:
        product = Products.query.get(Sno)
        qty_list = quantity.query.filter_by(ProductID=Sno).all()
        current_qty = []
        for qty in qty_list:
            current_qty.append(qty.Quantity)
        if request.method == "POST":
            # Update product details
            product.type = request.form["Type"]
            product.title = request.form["title"]
            product.title2 = request.form["title2"]
            product.title3 = request.form["title3"]
            product.purchesepr = request.form["purchesepr"]
            product.retailpr = request.form["retailpr"]
            product.wholepr = request.form["wholepr"]

            # Update product quantity in each location
            for loc in locations.query.all():
                qty = request.form[f"qty_{loc.LocationID}"]
                product_qty = quantity.query.filter_by(ProductID=Sno, LocationID=loc.LocationID).first()
                if product_qty is None:
                    product_qty = quantity(LocationID=loc.LocationID, ProductID=Sno, Quantity=qty)
                    db.session.add(product_qty)
                else:
                    product_qty.Quantity = qty
                db.session.commit()

            flash('Product updated successfully!', 'success')
            return redirect(url_for("showdata"))
        else:
            return render_template("update.html", product=product, loc=locations.query.all(),current_qty=current_qty)



@app.route('/login',methods =["POST","GET"])
def login():
        error= None
        if request.method == 'POST':
        # Get the username and password from the form
            username = request.form['user']
            password = request.form['Password']

        # Check if the user exists in the database
            user1 = user.query.filter_by(name=username, Password=password).first()
            if user1:
            # Set the session user based on the is_superuser field
                if user1.is_superuser:
                    session['user'] = 'super'
                else:
                    session['user'] = 'common'
                return redirect(url_for("home"))
            else:
                error="Wrong name Or password"
            return render_template('login.html', error=error)

        return render_template('login.html',error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        phone = request.form['phone']
        User = user(name=name, Password=password, phoneno=phone)
        db.session.add(User)
        db.session.commit()
        flash ('User created successfully!')
        return redirect(url_for("login"))
    else:
        return render_template('signup.html')

@app.route('/showdata')
def showdata():
    if 'user' not in session:
        return redirect(url_for('login'))
    elif session.get('user')=='super':
        products = db.session.query(Products).all()
        alocations = db.session.query(locations).all()
        data = []
        for product in products:
            row = {'Sno': product.Sno, 'Type': product.type, 'Company': product.title, 'Name': product.title2, 'S-Number': product.title3, 'Purchase price': product.purchesepr, 'Retail price': product.retailpr, 'Wholesale price': product.wholepr, 'Total_Quantity': 0}
            for location in alocations:
                total_qty = 0
                qty = db.session.query(quantity).filter_by(ProductID=product.Sno, LocationID=location.LocationID).first()
                if qty:
                    row[location.locationName] = qty.Quantity
                    row['Total_Quantity'] += qty.Quantity
                else:
                    row[location.locationName] = 0
            print (row['Total_Quantity'])
            data.append(row)
        # return render_template("tables.html", values=data, locations=alocations)
        return render_template("tables.html",a=data,locations=alocations)
    else:
        flash ('You are not authorized to access this page.')
        # Redirect to another route with an error message
        return redirect(url_for('home'))




@app.route('/low_quantity_products', methods=['GET', 'POST'])
def low_quantity_products():
    location_id = 1  # ID of the first location
    products = db.session.query(Products, quantity).join(quantity, Products.Sno == quantity.ProductID).filter(quantity.LocationID == location_id).filter(quantity.Quantity < 10).all()
    other_locations = locations.query.filter(locations.LocationID != location_id).all()

    if request.method == 'POST':
        product_id = request.form['product_id']
        quantity_to_move = int(request.form['quantity'])
        from_location_id = int(request.form['location'])
        to_location_id = 1  # ID of the first location

        # Get the product and its quantity in the selected location
        product_to_move = Products.query.filter_by(Sno=product_id).first()
        quantity_in_from_location = quantity.query.filter_by(LocationID=from_location_id, ProductID=product_id).first()

        # Calculate the new quantity in the from location and to location
        new_quantity_in_from_location = quantity_in_from_location.Quantity - quantity_to_move
        new_quantity_in_to_location = quantity.query.filter_by(LocationID=to_location_id, ProductID=product_id).first().Quantity + quantity_to_move

        # Make sure the new quantity in the from location is greater than or equal to 0
        if new_quantity_in_from_location < 0:
            flash('Not enough quantity to move', 'error')
            return redirect(url_for('low_quantity_products'))

        # Update the quantity in the from location and to location
        quantity_in_from_location.Quantity = new_quantity_in_from_location
        quantity.query.filter_by(LocationID=to_location_id, ProductID=product_id).first().Quantity = new_quantity_in_to_location
        db.session.commit()

        from_location_name = locations.query.filter_by(LocationID=from_location_id).first().locationName
        to_location_name = locations.query.filter_by(LocationID=to_location_id).first().locationName

        flash(f'{quantity_to_move} {product_to_move.title} moved from {from_location_name} to {to_location_name}', 'success')
        return redirect(url_for('low_quantity_products'))
    # Get available quantities for each product and location
    avail_qty = {}
    for product, qty in products:
        for loc in other_locations:
            key = f"{product.Sno}_{loc.LocationID}"
            qty_obj = quantity.query.filter_by(LocationID=loc.LocationID, ProductID=product.Sno).first()
            avail_qty[key] = qty_obj.Quantity if qty_obj else 0
    return render_template('low_quantity_products.html', results=products, other_locations=other_locations,avail_qty=avail_qty)

@app.route("/delete/<int:Sno>", methods=["GET"])
def delete_product(Sno):
    # Delete the product from the Quantity table for all locations.
    db.session.query(quantity).filter_by(ProductID=Sno).delete()

    # Delete the product from the Products table.
    product = Products.query.get(Sno)
    db.session.delete(product)
    db.session.commit()

    # Redirect the user to the main page.
    return redirect(url_for("showdata"))

@app.route('/logout')
def logout():
    session.pop("user", None)
    # flash("You are G O N E!", "Error")
    return redirect(url_for("login"))
if __name__ == '__main__':
    app.run(debug=True)
