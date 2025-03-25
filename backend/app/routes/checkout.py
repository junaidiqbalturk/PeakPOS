from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.checkout import Checkout

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    """API endpoint to process checkout"""
    user_id = get_jwt_identity()  # Get logged-in user ID
    response, status_code = Checkout.process_checkout(user_id)
    return jsonify(response), status_code
