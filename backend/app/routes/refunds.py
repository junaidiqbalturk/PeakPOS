from flask import Blueprint, request, jsonify
from app import db
from app.models.refund import Refund
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

refund_bp = Blueprint("refund", __name__)


# Get All Pending Refunds (Admin Only)
@refund_bp.route("/refunds", methods=["GET"])
@jwt_required()
def get_pending_refunds():
    """Retrieve all pending refunds (Admin only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized. Only admins can view refunds."}), 403

    pending_refunds = Refund.query.filter_by(status="Pending").all()
    return jsonify([refund.to_dict() for refund in pending_refunds]), 200


# Process Refund (Admin Only)
@refund_bp.route("/refunds/<int:refund_id>", methods=["PUT"])
@jwt_required()
def process_refund(refund_id):
    """Mark a refund as completed"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role != "admin":
        return jsonify({"error": "Unauthorized. Only admins can process refunds."}), 403

    refund = Refund.query.get(refund_id)
    if not refund:
        return jsonify({"error": "Refund not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Completed"]:
        return jsonify({"error": "Invalid status. Use 'Completed'."}), 400

    refund.status = new_status
    db.session.commit()

    return jsonify({"message": f"Refund {new_status} successfully", "refund": refund.to_dict()}), 200
