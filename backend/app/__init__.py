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
    Migrate(app, db)  # Add this to enable migrations
    jwt.init_app(app)
  #  CORS(app, resources={r"/api/*": {"origins": "*"}},  supports_credentials=True)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.product import product_bp  # Import product routes
    from app.routes.category import category_bp  # Register Category API
    from app.routes.order import order_bp  # Register Order Route
    from app.routes.supplier import supplier_bp  # Supplier Order API
    from app.routes.product_supplier import product_supplier_bp  # product_supplier API endpoint
    from app.routes.restocking import restocking_bp  # Import Restocking API
    from app.routes.inventory import inventory_bp  # Import Adjustment API
    from app.routes.cart import cart_bp  # Import Cart API
    from app.routes.checkout import checkout_bp  # Import Checkout API
    from app.routes.report import report_bp  # Import Reports API
    from app.routes.activity_log import activity_log_bp  # Import Activity Log API
    from app.routes.discount import discount_bp  # Import Activity Log API
    from app.routes.returns import returns_bp  # Import Returns  API
    from app.routes.refunds import refund_bp  # Import refund API
    from app.routes.receipt import receipt_bp  #Import Receipt API
    from app.routes.receipt_settings import receipt_settings_bp # Import Receipt Setting API

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api")  # Register products API
    app.register_blueprint(category_bp, url_prefix="/api")  # Register Categories API
    app.register_blueprint(order_bp, url_prefix="/api")  # Register Order API
    app.register_blueprint(supplier_bp, url_prefix="/api")  # Supplier API
    app.register_blueprint(product_supplier_bp, url_prefix="/api")  # product_supplier API
    app.register_blueprint(restocking_bp, url_prefix="/api")  # Register API
    app.register_blueprint(inventory_bp, url_prefix="/api")  # Inventory Adjustment API
    app.register_blueprint(cart_bp, url_prefix="/api")  # Register Cart API
    app.register_blueprint(checkout_bp, url_prefix="/api")  # Register Checkout API
    app.register_blueprint(report_bp, url_prefix="/api")  # Register Reports API
    app.register_blueprint(activity_log_bp, url_prefix="/api")  # Register Activity Log API
    app.register_blueprint(discount_bp, url_prefix="/api")  # Register discount API
    app.register_blueprint(returns_bp, url_prefix="/api")  # Register R3turns API
    app.register_blueprint(refund_bp, url_prefix="/api")  # Register Refund API
    app.register_blueprint(receipt_bp, url_prefix="/api")  # Register Receipt API
    app.register_blueprint(receipt_settings_bp, url_prefix="/api")  # Register Receipt Settings API
    from app.models import User, Product, Category, Order, OrderItem, supplier, activity_log

    # Test route
    @app.route("/api/hello", methods=["GET"])
    def hello():
        return jsonify({"message": "Welcome to PeakPOS API!"})

    @app.route('/test-image')
    def test_image():
        """Test route to verify static file serving"""
        return send_from_directory('static/product_images', 'FBK36CA1.webp')



    return app
