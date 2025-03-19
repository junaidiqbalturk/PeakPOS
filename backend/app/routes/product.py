from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product

product_bp = Blueprint("product", __name__)


# Create Product
@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    product = Product(name=data["name"], price=data["price"], stock=data["stock"], category_id=data["category_id"], )
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


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product.to_dict()), 200


@product_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    # Update product fields if provided
    if "name" in data:
        product.name = data["name"]
    if "price" in data:
        product.price = float(data["price"])
    if "stock" in data:
        product.stock = int(data["stock"])
    if "category" in data:
        product.category = data["category"]
    if "image_url" in data:
        product.image_url = data["image_url"]

    db.session.commit()

    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200


@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200
