import os
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    # Allow localhost/127.0.0.1 on common frontend dev ports (8080, 8081, 5173)
    env_origins = os.getenv("CORS_ORIGINS")
    if env_origins:
        allowed_origins = [o.strip() for o in env_origins.split(",") if o.strip()]
    else:
        allowed_origins = [
            "http://localhost:8080",
            "http://127.0.0.1:8080",
            "http://localhost:8081",
            "http://127.0.0.1:8081",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}}, supports_credentials=True)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.product import product_bp
    from app.routes.category import category_bp
    from app.routes.order import order_bp
    from app.routes.supplier import supplier_bp
    from app.routes.product_supplier import product_supplier_bp
    from app.routes.restocking import restocking_bp
    from app.routes.inventory import inventory_bp
    from app.routes.cart import cart_bp
    from app.routes.checkout import checkout_bp
    from app.routes.report import report_bp
    from app.routes.activity_log import activity_log_bp
    from app.routes.discount import discount_bp
    from app.routes.returns import returns_bp
    from app.routes.refunds import refund_bp
    from app.routes.receipt import receipt_bp
    from app.routes.receipt_settings import receipt_settings_bp
    from app.routes.tenant import tenant_bp
    from app.routes.user import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(category_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(supplier_bp, url_prefix="/api")
    app.register_blueprint(product_supplier_bp, url_prefix="/api")
    app.register_blueprint(restocking_bp, url_prefix="/api")
    app.register_blueprint(inventory_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(checkout_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")
    app.register_blueprint(activity_log_bp, url_prefix="/api")
    app.register_blueprint(discount_bp, url_prefix="/api")
    app.register_blueprint(returns_bp, url_prefix="/api")
    app.register_blueprint(refund_bp, url_prefix="/api")
    app.register_blueprint(receipt_bp, url_prefix="/api")
    app.register_blueprint(receipt_settings_bp, url_prefix="/api")
    app.register_blueprint(tenant_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")

    # Serve static product images and receipt logos safely
    @app.route("/static/product_images/<path:filename>")
    def serve_product_image(filename):
        return send_from_directory(os.path.join(app.root_path, "static", "product_images"), filename)

    @app.route("/static/receipt_logos/<path:filename>")
    def serve_receipt_logo(filename):
        return send_from_directory(os.path.join(app.root_path, "static", "receipt_logos"), filename)

    # Health check test route
    @app.route("/api/hello", methods=["GET"])
    def hello():
        return jsonify({"message": "Welcome to PeakPOS API!"})

    return app
