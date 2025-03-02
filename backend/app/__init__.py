from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Allow frontend to communicate with backend

    @app.route('/api/hello', methods=['GET'])
    def hello():
        return {"message": "Welcome to PeakPOS API!"}

    return app
