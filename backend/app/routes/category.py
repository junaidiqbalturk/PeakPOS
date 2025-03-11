from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["POST"])
def add_category():
    data = request.get_json()

    # Validate data
    if not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    # Check if category already exists
    existing_category = Category.query.filter_by(name=data["name"]).first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400

    # Create new category
    new_category = Category(name=data["name"])

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category added successfully", "category": new_category.to_dict()}), 201


@category_bp.route("/categories", methods=["GET"])
def get_categories():
    categories = Category.query.all()

    if not categories:
        return jsonify([])  # Return an empty list if no categories exist

    return jsonify([category.to_dict() for category in categories]), 200


@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()

    if "name" in data:
        # Check if category name already exists
        existing_category = Category.query.filter_by(name=data["name"]).first()
        if existing_category and existing_category.id != category_id:
            return jsonify({"error": "Category name already exists"}), 400

        category.name = data["name"]

    db.session.commit()

    return jsonify({"message": "Category updated successfully", "category": category.to_dict()}), 200


@category_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200
