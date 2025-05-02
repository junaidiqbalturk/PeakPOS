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
    """Process checkout with an optional discount_id from the frontend."""
    user_id = get_jwt_identity()
    cart = Cart.get_cart()

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    data = request.get_json()
    discount_id = data.get("discount_id")
    total_price = 0
    order_items = []
    applied_discount = None

    # Try to fetch the discount if discount_id is provided
    if discount_id:
        discount = Discount.query.filter_by(id=discount_id, active=True).first()
        if discount:
            applied_discount = discount.to_dict()
    else:
        # Optional: fallback to first active discount (legacy behavior)
        discount = Discount.query.filter_by(active=True).first()
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

    new_order = Order(user_id=user_id, total_price=total_price)
    db.session.add(new_order)
    db.session.flush()

    for item in order_items:
        item.order_id = new_order.id
        db.session.add(item)

    db.session.commit()
    Cart.clear_cart()

    return jsonify({
        "message": "Checkout successful",
        "order_id": new_order.id,
        "discount_applied": applied_discount
    }), 201
