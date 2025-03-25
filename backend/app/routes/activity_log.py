from flask import Blueprint, jsonify, request
from app import db
from app.models.activity_log import ActivityLog
from flask_jwt_extended import jwt_required, get_jwt_identity

activity_log_bp = Blueprint("activity_log", __name__)


# ✅ Get all activity logs (Admin only)
@activity_log_bp.route("/activity-logs", methods=["GET"])
@jwt_required()
def get_activity_logs():
    logs = ActivityLog.query.all()
    return jsonify([log.to_dict() for log in logs]), 200


# ✅ Create an activity log entry (For Testing)
@activity_log_bp.route("/activity-logs", methods=["POST"])
@jwt_required()
def create_activity_log():
    data = request.get_json()
    user_id = get_jwt_identity()

    if not data.get("action"):
        return jsonify({"error": "Action is required"}), 400

    log_entry = ActivityLog(user_id=user_id, action=data["action"])
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({"message": "Activity log created successfully"}), 201
