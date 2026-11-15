from flask import Blueprint, request, jsonify
from app.models import Order, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.receipt import Receipt

receipt_bp = Blueprint("receipt", __name__)

@receipt_bp.route("/receipts", methods=["GET"])
@jwt_required()
def get_all_receipts():
    """Retrieve all receipts sorted latest first."""
    receipts = Receipt.query.order_by(Receipt.created_at.desc()).limit(50).all()
    return jsonify([{
        "receipt_id": r.id,
        "order_id": r.order_id,
        "created_at": r.created_at.isoformat() if r.created_at else None,
        "created_by": r.created_by,
        "snapshot": r.snapshot
    } for r in receipts]), 200

@receipt_bp.route("/receipts", methods=["POST"])
@jwt_required()
def create_receipt():
    data = request.get_json() or {}
    order_id = data.get("order_id")
    snapshot = data.get("snapshot")

    # validation of input
    if not order_id or not snapshot:
        return jsonify({"error": "Order ID and Receipt Snapshot is required"}), 400

    existing = Receipt.query.filter_by(order_id=order_id).first()
    if existing:
        return jsonify({"error": "Receipt already exists for this order", "receipt_id": existing.id}), 200

    receipt = Receipt(
        order_id=order_id,
        snapshot=snapshot,
        created_by=get_jwt_identity()
    )
    db.session.add(receipt)
    db.session.commit()

    return jsonify({"message": "Receipt created successfully", "receipt_id": receipt.id}), 201


@receipt_bp.route('/receipts/<int:order_id>', methods=['GET'])
@jwt_required()
def get_receipt_by_order(order_id):
    receipt = Receipt.query.filter_by(order_id=order_id).first()
    if not receipt:
        # Fallback: check if the queried ID is directly the receipt primary key
        receipt = Receipt.query.get(order_id)
        if not receipt:
            return jsonify({"error": "No Receipt found"}), 404

    return jsonify({
        "receipt_id": receipt.id,
        "order_id": receipt.order_id,
        "created_at": receipt.created_at.isoformat() if receipt.created_at else None,
        "created_by": receipt.created_by,
        "snapshot": receipt.snapshot
    }), 200
