from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(username=data["username"], email=data["email"], role=data.get("role", "cashier"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Check if email is provided
    if not data or not data.get("email"):
        return jsonify({"error": "Email is required"}), 400

    # Check if password is provided
    if not data.get("password"):
        return jsonify({"error": "Password is required"}), 400

    # Find user by email
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        # Create JWT token with an expiration time (for enhanced security)
        expires = datetime.timedelta(days=1)  # Token valid for 1 day
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=expires
        )

        # Log successful login
        print(f"User {user.username} (ID: {user.id}, Role: {user.role}) logged in successfully")

        # Return token and role
        return jsonify({
            "token": access_token,
            "role": user.role,
            "username": user.username
        }), 200

    # Invalid credentials
    return jsonify({"error": "Invalid email or password"}), 401


@auth_bp.route("/user/me", methods=["GET", "OPTIONS"])
def get_user():
    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200

    # FIXED: Correctly apply jwt_required decorator
    @jwt_required()
    def protected_get_user():
        # Get user ID from JWT identity
        user_id = get_jwt_identity()

        # Find user by ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Return user data (exclude sensitive information)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }), 200

    # Call the nested function
    return protected_get_user()


# ADDITIONAL: Add logout endpoint (JWT token should be invalidated on client-side)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Client should remove the token from storage
    # For enhanced security, you could implement a token blacklist
    # This is a simple implementation
    user_id = get_jwt_identity()
    print(f"User {user_id} logged out")
    return jsonify({"message": "Logged out successfully"}), 200