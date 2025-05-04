from flask import Blueprint, request, jsonify
from app import db
from app.models.discount import Discount
from flask_jwt_extended import jwt_required

discount_bp = Blueprint("discount", __name__)


# Create Discount
@discount_bp.route("/discounts", methods=["POST"])
@jwt_required()
def add_discount():
    data = request.get_json()

    if "name" not in data or "discount_type" not in data or "value" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if data["discount_type"] not in ["percentage", "fixed"]:
        return jsonify({"error": "Invalid discount type"}), 400

    discount = Discount(
        name=data["name"],
        discount_type=data["discount_type"],
        value=data["value"]
    )
    db.session.add(discount)
    db.session.commit()

    return jsonify({"message": "Discount added successfully", "discount": discount.to_dict()}), 201


# Get All Discounts
@discount_bp.route("/discounts", methods=["GET"])
#@jwt_required()
def get_discounts():
    discounts = Discount.query.all()
    return jsonify([discount.to_dict() for discount in discounts]), 200


# Get Single Discount by ID
@discount_bp.route("/discounts/<int:discount_id>", methods=["GET"])
@jwt_required()
def get_discount(discount_id):
    discount = Discount.query.get(discount_id)
    if not discount:
        return jsonify({"error": "Discount not found"}), 404
    return jsonify(discount.to_dict()), 200


# Update Discount
@discount_bp.route("/discounts/<int:discount_id>", methods=["PUT"])
@jwt_required()
def update_discount(discount_id):
    discount = Discount.query.get(discount_id)
    if not discount:
        return jsonify({"error": "Discount not found"}), 404

    data = request.get_json()

    if "name" in data:
        discount.name = data["name"]
    if "discount_type" in data and data["discount_type"] in ["percentage", "fixed"]:
        discount.discount_type = data["discount_type"]
    if "value" in data:
        discount.value = data["value"]
    if "active" in data:
        discount.active = data["active"]

    db.session.commit()
    return jsonify({"message": "Discount updated successfully", "discount": discount.to_dict()}), 200


# Delete Discount
@discount_bp.route("/discounts/<int:discount_id>", methods=["DELETE"])
@jwt_required()
def delete_discount(discount_id):
    discount = Discount.query.get(discount_id)
    if not discount:
        return jsonify({"error": "Discount not found"}), 404

    db.session.delete(discount)
    db.session.commit()

    return jsonify({"message": "Discount deleted successfully"}), 200
