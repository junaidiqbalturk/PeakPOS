from flask import Blueprint, request, jsonify
from app import db
from app.models.product import Product
from app.models.inventory_adjustment import InventoryAdjustment
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.models.user import User

inventory_bp = Blueprint("inventory", __name__)


def admin_required(fn):
    """Decorator to restrict access to Admin users only."""

    @wraps(fn)  # Preserve original function name
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403  # Forbidden

        return fn(*args, **kwargs)

    return wrapper  # Return the wrapped function


@inventory_bp.route("/inventory/adjust", methods=["POST"])
@admin_required
def adjust_inventory():
    """Manually adjust stock for a product"""
    data = request.get_json()

    product = Product.query.get(data["product_id"])
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if data["adjustment_type"] not in ["increase", "decrease"]:
        return jsonify({"error": "Invalid adjustment type. Must be 'increase' or 'decrease'."}), 400

    if data["quantity_changed"] <= 0:
        return jsonify({"error": "Quantity must be greater than zero"}), 400

    if data["adjustment_type"] == "decrease" and product.stock < data["quantity_changed"]:
        return jsonify({"error": "Not enough stock available"}), 400

    # Adjust stock
    if data["adjustment_type"] == "increase":
        product.stock += data["quantity_changed"]
    else:
        product.stock -= data["quantity_changed"]

    # Log the adjustment
    adjustment = InventoryAdjustment(
        product_id=product.id,
        admin_id=get_jwt_identity(),
        adjustment_type=data["adjustment_type"],
        quantity_changed=data["quantity_changed"],
        reason=data.get("reason", "Manual adjustment"),
    )

    db.session.add(adjustment)
    db.session.commit()

    return jsonify({"message": "Stock updated successfully"}), 200
