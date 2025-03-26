from flask import Blueprint, request, jsonify
from app import db
from app.models.returns import Return
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User  # Import User model
from app.models.refund import Refund # Import Refund model
from flask_jwt_extended import jwt_required, get_jwt_identity

returns_bp = Blueprint("returns", __name__)

# 1️⃣ Create a Return Request (Cashier)
@returns_bp.route("/returns", methods=["POST"])
@jwt_required()
def request_return():
    """Cashier initiates a return request for an order item."""
    user_id = get_jwt_identity()
    data = request.get_json()

    order_id = data.get("order_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    reason = data.get("reason")

    if not order_id or not product_id or not quantity or not reason:
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the order and product exist
    order_item = OrderItem.query.filter_by(order_id=order_id, product_id=product_id).first()
    if not order_item:
        return jsonify({"error": "Order item not found"}), 404

    # Validate return quantity
    if quantity > order_item.quantity:
        return jsonify({"error": "Return quantity exceeds purchased quantity"}), 400

    # Calculate refund amount
    refund_amount = order_item.price_at_purchase * quantity

    # Create Return Entry
    return_request = Return(
        order_id=order_id,
        product_id=product_id,
        user_id=user_id,  # ✅ Associate return with the cashier
        quantity=quantity,
        refund_amount=refund_amount,
        reason=reason,
        status="Pending"
    )

    db.session.add(return_request)
    db.session.commit()

    return jsonify({"message": "Return request submitted successfully", "return": return_request.to_dict()}), 201


# 2️⃣ Get All Return Requests (Restricted by Role)
@returns_bp.route("/returns", methods=["GET"])
@jwt_required()
def get_returns():
    """Admins see all returns; Cashiers only see their own returns."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role == "admin":
        # ✅ Admin sees all return requests
        returns = Return.query.all()
    else:
        # ✅ Cashier sees only their own returns
        returns = Return.query.filter_by(user_id=user_id).all()

    return_list = [
        {
            "id": ret.id,
            "order_id": ret.order_id,
            "product_id": ret.product_id,
            "quantity": ret.quantity,
            "refund_amount": ret.refund_amount,
            "reason": ret.reason,
            "status": ret.status,
            "created_at": ret.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for ret in returns
    ]

    return jsonify(return_list), 200


@returns_bp.route("/returns/<int:return_id>", methods=["PUT"])
@jwt_required()
def process_return(return_id):
    """Admin approves or rejects a return request."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized. Only admins can process returns."}), 403

    return_request = Return.query.get(return_id)
    if not return_request:
        return jsonify({"error": "Return request not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Approved", "Rejected"]:
        return jsonify({"error": "Invalid status. Use 'Approved' or 'Rejected'."}), 400

    return_request.status = new_status

    # ✅ If approved, update stock and create refund entry
    if new_status == "Approved":
        product = Product.query.get(return_request.product_id)
        if product:
            product.stock += return_request.quantity  # ✅ Restock product

        # ✅ Create refund entry
        refund = Refund(
            return_id=return_request.id,
            user_id=return_request.user_id,
            refund_amount=return_request.refund_amount,
            status="Pending"  # ✅ Refund will be processed later
        )
        db.session.add(refund)

    db.session.commit()
    return jsonify({"message": f"Return request {new_status} successfully", "return": return_request.to_dict()}), 200
