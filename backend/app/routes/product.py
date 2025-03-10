from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

product_bp = Blueprint("product", __name__)


# Create Product
@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product = Product(name=data["name"], price=data["price"], stock=data["stock"])
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201


# Get All Products
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify([])  #Return an empty JSON list instead of None
    return jsonify([product.to_dict() for product in products])
