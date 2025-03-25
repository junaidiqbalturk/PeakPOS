from idlelib.configdialog import changes

from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import OrderItem  # Correct import
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.activity_log import log_activity  # Import log function

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


# Product Update Single or Multiple Attributes of the Products

@product_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    """Update product details (Admins Only)"""
    data = request.get_json()
    user_id = get_jwt_identity()

    # 🔐 Check if user is an admin
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    # 🔍 Find the product
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # ✅ Update fields if present in request
    if "name" in data:
        product.name = data["name"]
    if "price" in data and data["price"] >= 0:
        product.price = float(data["price"])
    if "stock" in data:
        if data["stock"] < 0:
            return jsonify({"error": "Stock cannot be negative"}), 400
        product.stock = int(data["stock"])
    if "category_id" in data:
        product.category_id = data["category_id"]
    if "image_url" in data:
        product.image_url = data["image_url"]

    db.session.commit()
    # Log the product update
    log_activity(user_id, "Updated Product", ", ".join(changes))
    return jsonify({"message": "Product updated successfully", "product": product.to_dict()}), 200


# Delete a specific Product using ID
@product_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"}), 200


# Sales of Products Endpoint

@product_bp.route("/products/sales", methods=["GET"])
@jwt_required()
def get_product_sales():
    products = Product.query.all()
    sales_data = []

    for product in products:
        total_sold = db.session.query(db.func.sum(OrderItem.quantity)).filter(
            OrderItem.product_id == product.id).scalar() or 0
        sales_data.append({
            "product_id": product.id,
            "name": product.name,
            "total_sold": total_sold
        })

    return jsonify(sales_data)


# Low Stock Notification Endpoint
@product_bp.route("/products/low-stock", methods=["GET"])
@jwt_required()
def get_low_stock_products():
    """Fetch products that are running low on stock"""
    threshold = request.args.get("threshold", 5, type=int)  # Default threshold = 5
    low_stock_products = Product.query.filter(Product.stock < threshold).all()

    return jsonify([product.to_dict() for product in low_stock_products]), 200


# Bulk Product Attribute Updates Endpoint
@product_bp.route("/products/bulk-update", methods=["PUT"])
@jwt_required()
def bulk_update_products():
    """Allow admin to update multiple products in a single request."""
    user_id = get_jwt_identity()  # Get logged-in user
    user = User.query.get(user_id)

    # Ensure only Admin can perform bulk updates
    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    if not isinstance(data, list):  # Ensure it's a list of products
        return jsonify({"error": "Invalid request format"}), 400

    updated_products = []
    errors = []

    for product_data in data:
        product_id = product_data.get("id")
        product = Product.query.get(product_id)

        if not product:
            errors.append({"product_id": product_id, "error": "Product not found"})
            continue

        # Update fields only if provided
        if "name" in product_data:
            product.name = product_data["name"]
        if "price" in product_data:
            product.price = float(product_data["price"])
        if "stock" in product_data:
            product.stock = int(product_data["stock"])
        if "category_id" in product_data:
            product.category_id = int(product_data["category_id"])
        if "image_url" in product_data:
            product.image_url = product_data["image_url"]

        updated_products.append(product)

    db.session.commit()

    return jsonify({
        "message": "Bulk product update successful",
        "updated_products": [product.to_dict() for product in updated_products],
        "errors": errors
    }), 200
