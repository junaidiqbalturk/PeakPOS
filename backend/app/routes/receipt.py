from flask import Blueprint, request, jsonify
from app.models import db, receipt, Order, User
from flask_jwt_extended import jwt_required, get_jwt_identity

receipt_bp = Blueprint("receipt", __name__, url_prefix="/api/receipts")

@receipt_bp.route("/", methods=["POST"])
@jwt_required()
def create_receipt():
    data = request.get_json()
    order_id = data.get("order_id")
    user_id = get_jwt_identity()
    snapshot = data.get("snapshot")

    #validation of input
    if not order_id or not snapshot:
        return jsonify({"error": "Order ID and Receipt Snapshot is required"}), 400

    existing = Receipt.query.filter_by(order_id=order_id).first()
    if existing:
        return jsonify({"error": "Receipt already exists for this order"}), 400

    receipt = Receipt(
        order_id = order_id,
        snapshot = snapshot,
        created_by = get_jwt_identity()
    )
    db.session.add(receipt)
    db.session.commit()

    return jsonify({"message": "Receipt created successfully","Receipt ID": receipt.id}), 201


@receipt_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_receipt_by_order(order_id):
    receipt = Receipt.query.filter_by(order_id=order_id).first()
    if not receipt:
        return jsonify({"error": "No Receipt found"}), 404

    return jsonify({
        "receipt_id": receipt.id,
        "created_at": receipt.created_at,
        "created_by": receipt.created_by,
        "snapshot": receipt.snapshot
    })
