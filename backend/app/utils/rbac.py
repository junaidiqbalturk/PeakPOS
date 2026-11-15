from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from app.models.user import User


def get_current_tenant_and_role():
    """Extracts tenant_id and role from verified JWT claims or DB fallback."""
    verify_jwt_in_request()
    claims = get_jwt()
    tenant_id = claims.get("tenant_id")
    role = claims.get("role")

    # If claims don't have tenant_id (legacy tokens), look up user in DB
    if not tenant_id:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            tenant_id = user.tenant_id
            role = user.role

    return tenant_id, role


def tenant_required():
    """Ensures request is authenticated and has an active tenant assigned."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            tenant_id, role = get_current_tenant_and_role()
            if not tenant_id and role != "super_admin":
                return jsonify({"error": "No tenant context found. Access denied."}), 403
            g.tenant_id = tenant_id
            g.user_role = role
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def roles_required(*allowed_roles):
    """Restricts route access to specific roles (super_admin always permitted)."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            tenant_id, role = get_current_tenant_and_role()
            if role != "super_admin" and role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden: You do not have permission to perform this action.",
                    "required_roles": list(allowed_roles),
                    "current_role": role
                }), 403
            g.tenant_id = tenant_id
            g.user_role = role
            return fn(*args, **kwargs)
        return wrapper
    return decorator
