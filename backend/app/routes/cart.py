from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import Cart
from app.models.product import Product
from app.models.activity_log import ActivityLog  # ✅ Import Activity Log model

cart_bp = Blueprint("cart", __name__)


# ✅ Add Product to Cart (with Activity Log)
@cart_bp.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()  # Get the logged-in user ID
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id or quantity <= 0:
        return jsonify({"error": "Invalid product ID or quantity"}), 400

    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Log Activity 🚀
    log_entry = ActivityLog(user_id=user_id, action=f"Added {quantity} of {product.name} to cart")
    db.session.add(log_entry)

    updated_cart = Cart.add_to_cart(product_id, quantity)
    db.session.commit()  # ✅ Commit the log to DB

    return jsonify({"message": "Product added to cart", "cart": updated_cart}), 200


# ✅ Remove Product from Cart (with Activity Log)
@cart_bp.route("/cart/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Log Activity 🚀
    log_entry = ActivityLog(user_id=user_id, action=f"Removed {product.name} from cart")
    db.session.add(log_entry)

    updated_cart = Cart.remove_from_cart(product_id)
    db.session.commit()  # ✅ Commit the log to DB

    return jsonify({"message": "Product removed from cart", "cart": updated_cart}), 200


# ✅ Clear Cart (with Activity Log)
@cart_bp.route("/cart/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    user_id = get_jwt_identity()

    # Log Activity 🚀
    log_entry = ActivityLog(user_id=user_id, action="Cleared the cart")
    db.session.add(log_entry)

    cleared_cart = Cart.clear_cart()
    db.session.commit()  # ✅ Commit the log to DB

    return jsonify({"message": "Cart cleared", "cart": cleared_cart}), 200


# Get Cart Endpoint
@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():
    return jsonify({"cart": Cart.get_cart()}), 200
