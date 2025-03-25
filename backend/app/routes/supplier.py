from flask import Blueprint, request, jsonify
from app import db
from app.models.supplier import Supplier
from flask_jwt_extended import jwt_required

supplier_bp = Blueprint("supplier", __name__)


# Create Supplier
@supplier_bp.route("/suppliers", methods=["POST"])
@jwt_required()
def add_supplier():
    """Add a new supplier"""
    data = request.get_json()

    if not data.get("name") or not data.get("contact") or not data.get("email") or not data.get("address"):
        return jsonify({"error": "Missing required fields"}), 400

        # Check if supplier already exists
    if Supplier.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Supplier with this email already exists"}), 400

    new_supplier = Supplier(
        name=data["name"],
        contact=data["contact"],
        email=data["email"],
        address=data["address"]
    )
    db.session.add(new_supplier)
    db.session.commit()

    return jsonify({"message": "Supplier added successfully", "supplier": new_supplier.to_dict()}), 201


# Get All Suppliers
@supplier_bp.route("/suppliers", methods=["GET"])
@jwt_required()
def get_suppliers():
    """Fetch all suppliers"""
    suppliers = Supplier.query.all()
    return jsonify([supplier.to_dict() for supplier in suppliers]), 200


# Get Supplier by ID
@supplier_bp.route("/suppliers/<int:supplier_id>", methods=["GET"])
@jwt_required()
def get_supplier_by_id(supplier_id):
    """Fetch a single supplier by ID"""
    supplier = Supplier.query.get(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    return jsonify(supplier.to_dict()), 200


# Update Supplier
@supplier_bp.route("/suppliers/<int:supplier_id>", methods=["PUT"])
@jwt_required()
def update_supplier(supplier_id):
    """Update supplier details"""
    supplier = Supplier.query.get(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    data = request.get_json()

    if "name" in data:
        supplier.name = data["name"]
    if "contact" in data:
        supplier.contact = data["contact"]
    if "email" in data:
        supplier.email = data["email"]
    if "address" in data:
        supplier.address = data["address"]

    db.session.commit()
    return jsonify({"message": "Supplier updated successfully", "supplier": supplier.to_dict()}), 200


# Delete Supplier
@supplier_bp.route("/suppliers/<int:supplier_id>", methods=["DELETE"])
@jwt_required()
def delete_supplier(supplier_id):
    """Delete a supplier"""
    supplier = Supplier.query.get(supplier_id)

    if not supplier:
        return jsonify({"error": "Supplier not found"}), 404

    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"message": "Supplier deleted successfully"}), 200
