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
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        print(f"User Role: {user.role}")
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"token": access_token, "role": user.role}), 200

    return jsonify({"error": "Invalid credentials"}), 401


from flask import jsonify, request


@auth_bp.route("/user/me", methods=["GET", "OPTIONS"])
def get_user():
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200

    from flask_jwt_extended import jwt_required, get_jwt_identity
    @jwt_required()
    def protected_route():
        user_id = get_jwt_identity()
        print("JWT Identity:", user_id)
        return jsonify({"username": "TestUser", "email": "test@example.com"}), 200

    return protected_route()
