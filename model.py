from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

model = Blueprint('model', __name__)
db = SQLAlchemy()

class Products(db.Model):
    __tablename__ = "Products"
    Sno = db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(255), nullable=False)
    title=db.Column(db.String(255), nullable=True)
    title2=db.Column(db.String(255), nullable=True)
    title3=db.Column(db.String(255), nullable=True)
    purchesepr=db.Column(db.Integer)
    retailpr=db.Column(db.Integer)
    wholepr=db.Column(db.Integer)

class locations(db.Model):
    __tablename__ = "locations"
    LocationID = db.Column(db.Integer,primary_key=True)
    locationName =db.Column(db.String(255),nullable=True)

class quantity(db.Model):
    __tablename__ = "quantity"
    QID = db.Column(db.Integer,primary_key=True)
    LocationID=db.Column(db.Integer,db.ForeignKey('locations.LocationID'))
    ProductID=db.Column(db.Integer,db.ForeignKey('Products.Sno'))
    Quantity=db.Column(db.Integer)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    Password = db.Column(db.String(255))
    phoneno = db.Column(db.String(25))
    is_superuser = db.Column(db.Boolean, default=False)

class customers(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255))
    CNICnumber = db.Column(db.String(15))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    debit = db.Column(db.Float)
    credit = db.Column(db.Float)
    reference = db.Column(db.String(255))
    detail = db.Column(db.String(255))
    debt_allowed =db.Column(db.Boolean, default=False)
    searchable =db.Column(db.Boolean, default=True)

class Sales(db.Model):
    __tablename__ = "Sales"
    orderid = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.Integer, db.ForeignKey('customers.id'))
    salesmanID = db.Column(db.Integer, db.ForeignKey('user.id'))
    selldate = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float)
    # sales_items = db.relationship('sales_Items', backref='Sales', lazy=True)

class sales_Items(db.Model):
    __tablename__ = "sales_items"
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('Sales.orderid'))
    product_id = db.Column(db.Integer, db.ForeignKey('Products.Sno'))
    quantity = db.Column(db.Integer)
    profit = db.Column(db.Float)

class Business(db.Model):
    __tablename__ = "Business"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
