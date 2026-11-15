from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.discount import Discount
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.activity_log import ActivityLog
from app.utils.rbac import get_current_tenant_and_role
from app import db

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    """Process checkout with cart data directly from the request."""
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    # Get cart items directly from request
    cart_items = data.get("cart", [])
    discount_id = data.get("discount_id")

    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    applied_discount = None
    if discount_id:
        discount = Discount.query.filter_by(id=discount_id, active=True).first()
        if discount:
            applied_discount = discount.to_dict()

    try:
        subtotal = 0.0
        order_items = []

        # Process and validate each item in the cart
        for item in cart_items:
            product = Product.query.get(item.get("id"))
            if not product:
                db.session.rollback()
                return jsonify({"error": f"Product ID {item.get('id')} not found"}), 404

            quantity = int(item.get("quantity", 0))
            if quantity <= 0:
                db.session.rollback()
                return jsonify({"error": f"Invalid quantity for {product.name}"}), 400

            if product.stock < quantity:
                db.session.rollback()
                return jsonify({"error": f"Not enough stock for {product.name}"}), 400

            product.stock -= quantity
            subtotal += product.price * quantity

            order_items.append(OrderItem(
                product_id=product.id,
                quantity=quantity,
                price_at_purchase=product.price
            ))

        # Calculate discount at the order level
        discount_amount = 0.0
        if applied_discount:
            if applied_discount.get("discount_type") == "percentage":
                discount_amount = subtotal * (applied_discount.get("value", 0) / 100.0)
            elif applied_discount.get("discount_type") == "fixed":
                discount_amount = min(float(applied_discount.get("value", 0)), subtotal)

        total_price = max(subtotal - discount_amount, 0.0)

        # Include tax if supplied by client
        tax = float(data.get("tax", 0.0)) if data.get("tax") is not None else 0.0
        if tax > 0:
            total_price += tax

        # Round to 2 decimal places for financial precision
        total_price = round(total_price, 2)

        # Create the new order with tenant_id
        tenant_id = None
        try:
            tenant_id, _ = get_current_tenant_and_role()
        except Exception:
            pass

        new_order = Order(
            tenant_id=tenant_id,
            user_id=user_id,
            total_price=total_price,
            discount_id=discount_id if applied_discount else None
        )
        db.session.add(new_order)
        db.session.flush()

        for o_item in order_items:
            o_item.order_id = new_order.id
            db.session.add(o_item)

        # Add activity log
        log_entry = ActivityLog(user_id=user_id, action="Placed order")
        db.session.add(log_entry)

        db.session.commit()

        return jsonify({
            "message": "Checkout successful",
            "order_id": new_order.id,
            "discount_applied": applied_discount,
            "discount_amount": round(discount_amount, 2),
            "subtotal": round(subtotal, 2),
            "tax": round(tax, 2),
            "total_price": total_price
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Checkout failed: {str(e)}"}), 500
