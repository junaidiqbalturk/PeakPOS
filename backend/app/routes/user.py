from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from app.utils.rbac import roles_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import re

user_bp = Blueprint("user_bp", __name__)


def get_current_tenant_id():
    claims = get_jwt()
    tenant_id = claims.get("tenant_id")
    if not tenant_id:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        tenant_id = user.tenant_id if user else 1
    return tenant_id


@user_bp.route("/users", methods=["GET"])
@jwt_required()
@roles_required("super_admin", "admin", "manager")
def list_users():
    tenant_id = get_current_tenant_id()
    users = User.query.filter_by(tenant_id=tenant_id).order_by(User.id.desc()).all()

    user_list = []
    for u in users:
        user_list.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "pin_code": u.pin_code,
            "has_pin": bool(u.pin_code and len(str(u.pin_code).strip()) == 4),
            "is_active": True if u.is_active is None else bool(u.is_active)
        })

    return jsonify({"users": user_list, "total": len(user_list)}), 200


@user_bp.route("/users", methods=["POST"])
@jwt_required()
@roles_required("super_admin", "admin")
def create_user():
    tenant_id = get_current_tenant_id()
    data = request.get_json() or {}

    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", "")).strip()
    role = str(data.get("role", "cashier")).strip().lower()
    pin_code = str(data.get("pin_code", "")).strip()

    if not username:
        return jsonify({"error": "Full Name / Username is required"}), 400

    if not email or "@" not in email:
        return jsonify({"error": "Valid email address is required"}), 400

    if not password or len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters long"}), 400

    if role not in ["cashier", "manager", "admin"]:
        role = "cashier"

    if pin_code:
        if not re.match(r"^\d{4}$", pin_code):
            return jsonify({"error": "PIN code must be exactly 4 digits (e.g. 1234)"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": f"A user with email '{email}' already exists"}), 409

    if User.query.filter_by(username=username).first():
        return jsonify({"error": f"A user with username '{username}' already exists"}), 409

    new_user = User(
        tenant_id=tenant_id,
        username=username,
        email=email,
        role=role,
        pin_code=pin_code if pin_code else None,
        is_active=True
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": f"Cashier/Staff '{username}' created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
            "has_pin": bool(new_user.pin_code),
            "is_active": new_user.is_active
        }
    }), 201


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@roles_required("super_admin", "admin")
def update_user(user_id):
    tenant_id = get_current_tenant_id()
    user = User.query.filter_by(id=user_id, tenant_id=tenant_id).first()

    if not user:
        return jsonify({"error": "User not found in your store"}), 404

    data = request.get_json() or {}

    if "username" in data:
        uname = str(data["username"]).strip()
        if uname and uname != user.username:
            existing = User.query.filter_by(username=uname).first()
            if existing and existing.id != user.id:
                return jsonify({"error": f"Username '{uname}' already taken"}), 409
            user.username = uname

    if "email" in data:
        uemail = str(data["email"]).strip().lower()
        if uemail and uemail != user.email:
            existing = User.query.filter_by(email=uemail).first()
            if existing and existing.id != user.id:
                return jsonify({"error": f"Email '{uemail}' already taken"}), 409
            user.email = uemail

    if "role" in data:
        new_role = str(data["role"]).strip().lower()
        if new_role in ["cashier", "manager", "admin"]:
            # Prevent demoting the only admin
            if user.role == "admin" and new_role != "admin":
                admin_count = User.query.filter_by(tenant_id=tenant_id, role="admin", is_active=True).count()
                if admin_count <= 1:
                    return jsonify({"error": "Cannot demote the only active Administrator"}), 400
            user.role = new_role

    if "pin_code" in data:
        pin = str(data["pin_code"]).strip()
        if pin:
            if not re.match(r"^\d{4}$", pin):
                return jsonify({"error": "PIN code must be exactly 4 digits"}), 400
            user.pin_code = pin
        else:
            user.pin_code = None

    if "password" in data and str(data["password"]).strip():
        pwd = str(data["password"]).strip()
        if len(pwd) < 4:
            return jsonify({"error": "Password must be at least 4 characters"}), 400
        user.set_password(pwd)

    if "is_active" in data:
        is_act = bool(data["is_active"])
        if not is_act and user.id == int(get_jwt_identity()):
            return jsonify({"error": "Cannot deactivate your own active account"}), 400
        user.is_active = is_act

    db.session.commit()

    return jsonify({
        "message": f"User '{user.username}' updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "pin_code": user.pin_code,
            "has_pin": bool(user.pin_code),
            "is_active": user.is_active
        }
    }), 200


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
@roles_required("super_admin", "admin")
def delete_user(user_id):
    tenant_id = get_current_tenant_id()
    caller_id = int(get_jwt_identity())

    if user_id == caller_id:
        return jsonify({"error": "You cannot delete your own account"}), 400

    user = User.query.filter_by(id=user_id, tenant_id=tenant_id).first()
    if not user:
        return jsonify({"error": "User not found in your store"}), 404

    # If user has orders or receipts attached, soft delete (deactivate)
    if user.receipts and len(user.receipts) > 0:
        user.is_active = False
        db.session.commit()
        return jsonify({"message": f"User '{user.username}' has historical receipts; deactivated instead of deleted."}), 200

    username = user.username
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"Cashier/Staff '{username}' deleted successfully"}), 200
