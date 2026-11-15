from flask import Blueprint, request, jsonify
from app import db
from app.models.tenant import Tenant
from app.models.user import User
from app.utils.rbac import roles_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

tenant_bp = Blueprint("tenant_bp", __name__)


@tenant_bp.route("/tenant/settings", methods=["GET"])
@jwt_required()
def get_tenant_settings():
    claims = get_jwt()
    tenant_id = claims.get("tenant_id")
    if not tenant_id:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        tenant_id = user.tenant_id if user else 1

    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        # Fallback to default tenant
        tenant = Tenant.query.first()
        if not tenant:
            return jsonify({"error": "Tenant record not found"}), 404

    return jsonify({
        "id": tenant.id,
        "name": tenant.name,
        "slug": tenant.slug,
        "business_type": tenant.business_type,
        "currency": tenant.currency or "PKR",
        "currency_symbol": tenant.currency_symbol or "Rs.",
        "tax_rate": tenant.tax_rate if tenant.tax_rate is not None else 7.0,
        "plan": tenant.plan or "starter",
        "status": tenant.status or "active"
    }), 200


@tenant_bp.route("/tenant/settings", methods=["PUT", "POST"])
@jwt_required()
@roles_required("super_admin", "admin")
def update_tenant_settings():
    claims = get_jwt()
    tenant_id = claims.get("tenant_id")
    if not tenant_id:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        tenant_id = user.tenant_id if user else 1

    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        tenant = Tenant.query.first()
        if not tenant:
            return jsonify({"error": "Tenant not found"}), 404

    data = request.get_json() or {}

    if "name" in data and data["name"]:
        tenant.name = str(data["name"]).strip()

    if "business_type" in data and data["business_type"]:
        tenant.business_type = str(data["business_type"]).strip()

    if "currency" in data and data["currency"]:
        tenant.currency = str(data["currency"]).strip().upper()

    if "currency_symbol" in data and data["currency_symbol"]:
        tenant.currency_symbol = str(data["currency_symbol"]).strip()

    if "tax_rate" in data:
        try:
            tenant.tax_rate = float(data["tax_rate"])
        except (ValueError, TypeError):
            pass

    db.session.commit()

    return jsonify({
        "message": "Store settings updated successfully",
        "tenant": tenant.to_dict()
    }), 200
