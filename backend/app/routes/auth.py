from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
import datetime

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields: username, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    # Role assignment security:
    # First user registered in the system is automatically 'admin' (bootstrap mode).
    # Subsequent public signups are strictly 'cashier' unless created by an authenticated admin.
    assigned_role = "cashier"
    user_count = User.query.count()
    requested_role = data.get("role", "cashier").strip().lower()

    if user_count == 0:
        assigned_role = "admin"
    elif requested_role == "admin":
        # Check if request has an authenticated admin token
        try:
            verify_jwt_in_request(optional=True)
            current_user_id = get_jwt_identity()
            if current_user_id:
                current_user = User.query.get(current_user_id)
                if current_user and current_user.role == "admin":
                    assigned_role = "admin"
        except Exception:
            pass  # Fall back to cashier

    user = User(username=username, email=email, role=assigned_role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=expires
        )

        return jsonify({
            "token": access_token,
            "role": user.role,
            "username": user.username
        }), 200

    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route("/user/me", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    return jsonify({"message": f"User {user_id} logged out successfully"}), 200
