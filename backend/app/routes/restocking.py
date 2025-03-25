from flask import Blueprint, request, jsonify
from app import db
from app.models.restocking import Restocking
from app.models.product import Product
from app.models.supplier import Supplier
from flask_jwt_extended import jwt_required

restocking_bp = Blueprint("restocking", __name__)


# Create a Restocking Request
@restocking_bp.route("/restocking", methods=["POST"])
@jwt_required()
def request_restocking():
    """Create a restocking request for a product"""
    data = request.get_json()

    if not all(key in data for key in ["product_id", "supplier_id", "quantity"]):
        return jsonify({"error": "Missing required fields"}), 400

    product = Product.query.get(data["product_id"])
    supplier = Supplier.query.get(data["supplier_id"])

    if not product or not supplier:
        return jsonify({"error": "Invalid product or supplier"}), 404

    restock = Restocking(
        product_id=product.id,
        supplier_id=supplier.id,
        quantity=data["quantity"],
        status="Pending"
    )

    db.session.add(restock)
    db.session.commit()

    return jsonify({"message": "Restocking request created successfully", "data": restock.to_dict()}), 201


# Get All Restocking Requests
@restocking_bp.route("/restocking", methods=["GET"])
@jwt_required()
def get_restocking_requests():
    """Fetch all restocking requests"""
    restocks = Restocking.query.all()
    return jsonify([r.to_dict() for r in restocks]), 200


# Approve or Reject a Restocking Request
@restocking_bp.route("/restocking/<int:id>", methods=["PUT"])
@jwt_required()
def update_restocking_status(id):
    """Update the status of a restocking request"""
    restock = Restocking.query.get(id)

    if not restock:
        return jsonify({"error": "Restocking request not found"}), 404

    data = request.get_json()
    if "status" in data:
        restock.status = data["status"]

        # If approved, update the product stock
        if restock.status == "Approved":
            product = Product.query.get(restock.product_id)
            product.stock += restock.quantity

    db.session.commit()
    return jsonify({"message": "Restocking request updated", "data": restock.to_dict()}), 200


# Delete a Restocking Request
@restocking_bp.route("/restocking/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_restocking_request(id):
    """Delete a restocking request"""
    restock = Restocking.query.get(id)

    if not restock:
        return jsonify({"error": "Restocking request not found"}), 404

    db.session.delete(restock)
    db.session.commit()
    return jsonify({"message": "Restocking request deleted"}), 200
