from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.checkout import Checkout
from app.models.discount import Discount
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app import db

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    """Process checkout by applying discounts (if available)."""
    user_id = get_jwt_identity()
    cart = Cart.get_cart()

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    total_price = 0
    order_items = []
    applied_discount = None

    # Check if a discount exists
    discount = Discount.query.filter_by(active=True).first()  # Example: Apply first active discount
    if discount:
        applied_discount = discount.to_dict()

    for item in cart:
        product = Product.query.get(item["product_id"])
        if not product:
            return jsonify({"error": f"Product ID {item['product_id']} not found"}), 404

        if product.stock < item["quantity"]:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400

        product.stock -= item["quantity"]

        item_price = product.price * item["quantity"]

        # Apply Discount Logic
        if applied_discount:
            if applied_discount["discount_type"] == "percentage":
                item_price -= (item_price * (applied_discount["value"] / 100))
            elif applied_discount["discount_type"] == "fixed":
                item_price -= applied_discount["value"]

        total_price += item_price
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item["quantity"],
            price_at_purchase=item_price
        ))

    # Create Order
    new_order = Order(user_id=user_id, total_price=total_price)
    db.session.add(new_order)
    db.session.flush()

    # Add order items
    for item in order_items:
        item.order_id = new_order.id
        db.session.add(item)

    db.session.commit()

    Cart.clear_cart()

    return jsonify(
        {"message": "Checkout successful", "order_id": new_order.id, "discount_applied": applied_discount}), 201