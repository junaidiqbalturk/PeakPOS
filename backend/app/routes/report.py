from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from datetime import datetime
from app.models.report import SalesReport

report_bp = Blueprint("report", __name__)


@report_bp.route("/sales-summary", methods=["GET"])
@jwt_required()
def sales_summary():
    """API to get total revenue & orders in a date range"""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    report = SalesReport.get_sales_summary(start_date, end_date)
    return jsonify(report), 200


@report_bp.route("/best-selling-products", methods=["GET"])
@jwt_required()
def best_selling_products():
    """API to get best-selling products"""
    limit = request.args.get("limit", default=5, type=int)
    best_sellers = SalesReport.get_best_selling_products(limit)
    return jsonify(best_sellers), 200
