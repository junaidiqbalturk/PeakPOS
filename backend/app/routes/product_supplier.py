from flask import Blueprint, request, jsonify
from app import db
from app.models.ProductSupplier import ProductSupplier
from flask_jwt_extended import jwt_required, get_jwt_identity

product_supplier_bp = Blueprint("product_supplier", __name__)


# Assign a Supplier to a Product
@product_supplier_bp.route("/product-supplier", methods=["POST"])
@jwt_required()
def assign_supplier():
    """Assigns a supplier to a product with price and supply date"""
    data = request.get_json()

    if not all(key in data for key in ["product_id", "supplier_id", "price"]):
        return jsonify({"error": "Missing required fields (product_id, supplier_id, price)"}), 400

    product_supplier = ProductSupplier(
        product_id=data["product_id"],
        supplier_id=data["supplier_id"],
        price=float(data["price"])
    )

    db.session.add(product_supplier)
    db.session.commit()

    return jsonify({"message": "Supplier assigned to product successfully", "data": product_supplier.to_dict()}), 201


# Get All Product-Supplier Relationships
@product_supplier_bp.route("/product-supplier", methods=["GET"])
@jwt_required()
def get_product_suppliers():
    """Fetch all product-supplier relationships"""
    relationships = ProductSupplier.query.all()
    return jsonify([relation.to_dict() for relation in relationships]), 200


# Update Supplier-Product Price or Supply Date
@product_supplier_bp.route("/product-supplier/<int:id>", methods=["PUT"])
@jwt_required()
def update_product_supplier(id):
    """Update price or supply date for a product-supplier relationship"""
    product_supplier = ProductSupplier.query.get(id)

    if not product_supplier:
        return jsonify({"error": "Product-Supplier relationship not found"}), 404

    data = request.get_json()

    if "price" in data:
        product_supplier.price = float(data["price"])
    if "supply_date" in data:
        product_supplier.supply_date = data["supply_date"]

    db.session.commit()
    return jsonify({"message": "Product-Supplier relationship updated", "data": product_supplier.to_dict()}), 200


# Remove a Supplier from a Product
@product_supplier_bp.route("/product-supplier/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product_supplier(id):
    """Remove a supplier from a product"""
    product_supplier = ProductSupplier.query.get(id)

    if not product_supplier:
        return jsonify({"error": "Product-Supplier relationship not found"}), 404

    db.session.delete(product_supplier)
    db.session.commit()
    return jsonify({"message": "Product-Supplier relationship deleted successfully"}), 200
