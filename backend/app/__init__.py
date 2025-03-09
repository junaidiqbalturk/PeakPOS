from flask import Flask, jsonify
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
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Import and register blueprints (FIXED IMPORT PATH)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # Test route
    @app.route("/api/hello", methods=["GET"])
    def hello():
        return jsonify({"message": "Welcome to PeakPOS API!"})

    return app
