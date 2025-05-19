from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.checkout import Checkout
from  app.models.discount import Discount
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app import db

from app.models.activity_log import ActivityLog

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    """Process checkout with cart data directly from the request."""
    user_id = get_jwt_identity()
    data = request.get_json()

    # Get cart items directly from request
    cart_items = data.get("cart", [])
    discount_id = data.get("discount_id")

    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    total_price = 0
    order_items = []
    applied_discount = None

    # Try to fetch the discount if discount_id is provided
    if discount_id:
        discount = Discount.query.filter_by(id=discount_id, active=True).first()
        if discount:
            applied_discount = discount.to_dict()

    # Process each item in the cart data from the client
    for item in cart_items:
        product = Product.query.get(item["id"])
        if not product:
            return jsonify({"error": f"Product ID {item['id']} not found"}), 404

        if product.stock < item["quantity"]:
            return jsonify({"error": f"Not enough stock for {product.name}"}), 400

        product.stock -= item["quantity"]
        item_price = product.price * item["quantity"]

        # Apply discount per item
        if applied_discount:
            if applied_discount["discount_type"] == "percentage":
                item_price *= (1 - applied_discount["value"] / 100)
            elif applied_discount["discount_type"] == "fixed":
                item_price -= applied_discount["value"]
                item_price = max(item_price, 0)  # Prevent negative price

        total_price += item_price
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item["quantity"],
            price_at_purchase=item_price
        ))

    # Create the new order
    new_order = Order(user_id=user_id, total_price=total_price, discount_id=discount_id if applied_discount else None)
    db.session.add(new_order)
    db.session.flush()

    for item in order_items:
        item.order_id = new_order.id
        db.session.add(item)

    # Add activity log
    log_entry = ActivityLog(user_id=user_id, action="Placed order")
    db.session.add(log_entry)

    db.session.commit()

    # No need to call Cart.clear_cart() since cart is managed client-side

    return jsonify({
        "message": "Checkout successful",
        "order_id": new_order.id,
        "discount_applied": applied_discount,
        "total_price": total_price
    }), 201