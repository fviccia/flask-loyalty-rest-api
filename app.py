from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Initialize DB
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)

# Product Class
class Product(db.Model):
    __tablename__ = "PRODUCTS"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price


# Client Class
class Client(db.Model):
    __tablename__ = "CLIENTS"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    points = db.Column(db.Float)

    def __init__(self, name, points):
        self.name = name
        self.points = points


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "price")


# Client Schema
class ClientSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "points")


# Create a product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]

    new_product = Product(name, description, price)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a product
@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    # Get the fields from the body of the request
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]

    # Set the new values on the product object
    product.name = name
    product.description = description
    product.price = price

    db.session.commit()

    return product_schema.jsonify(product)


# Delete single product
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    # Always commit after you do some change
    db.session.commit()
    return product_schema.jsonify(product)


# Initialize Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# NOTE: To initiliaze the db we have to open a python terminal the we write
#  "from app import db" the we usen the function "db.create_all()"

# Run Server
if __name__ == "__main__":
    app.run(debug=True)
