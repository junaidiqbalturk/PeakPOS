from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from app.utils.rbac import get_current_tenant_and_role, roles_required
from flask_jwt_extended import jwt_required

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["POST"])
@jwt_required()
@roles_required("super_admin", "admin", "manager")
def add_category():
    data = request.get_json() or {}
    tenant_id = None
    try:
        tenant_id, _ = get_current_tenant_and_role()
    except Exception:
        pass

    # Validate data
    if not data.get("name"):
        return jsonify({"error": "Category name is required"}), 400

    # Check if category already exists in this tenant
    query = Category.query.filter_by(name=data["name"])
    if tenant_id:
        query = query.filter_by(tenant_id=tenant_id)
    existing_category = query.first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 400

    # Create new category
    new_category = Category(name=data["name"], tenant_id=tenant_id)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "Category added successfully", "category": new_category.to_dict()}), 201


@category_bp.route("/categories", methods=["GET"])
def get_categories():
    try:
        tenant_id, role = get_current_tenant_and_role()
        if tenant_id and role != "super_admin":
            categories = Category.query.filter_by(tenant_id=tenant_id).all()
        else:
            categories = Category.query.all()
    except Exception:
        categories = Category.query.all()

    if not categories:
        return jsonify([])

    return jsonify([category.to_dict() for category in categories]), 200


@category_bp.route("/categories/<int:category_id>", methods=["PUT"])
@jwt_required()
@roles_required("super_admin", "admin", "manager")
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
@jwt_required()
@roles_required("super_admin", "admin", "manager")
def delete_category(category_id):
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200
