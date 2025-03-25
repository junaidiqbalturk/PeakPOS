from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required
from app.models.cart import Cart
from app.models.product import Product

cart_bp = Blueprint("cart", __name__)


# Add Product to Cart
@cart_bp.route("/cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id or quantity <= 0:
        return jsonify({"error": "Invalid product ID or quantity"}), 400

    # Check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    updated_cart = Cart.add_to_cart(product_id, quantity)
    return jsonify({"message": "Product added to cart", "cart": updated_cart}), 200


# Remove Product from Cart
@cart_bp.route("/cart/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    updated_cart = Cart.remove_from_cart(product_id)
    return jsonify({"message": "Product removed from cart", "cart": updated_cart}), 200


# Get Cart Items
@cart_bp.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():
    return jsonify({"cart": Cart.get_cart()}), 200


# Clear Cart
@cart_bp.route("/cart/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    return jsonify({"message": "Cart cleared", "cart": Cart.clear_cart()}), 200
