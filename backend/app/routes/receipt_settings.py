# routes/receipt_settings.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app import db
import logging
from app.models.receipt_settings import ReceiptSettings
from app.utils.rbac import roles_required
from flask_jwt_extended import jwt_required

receipt_settings_bp = Blueprint('receipt_settings_bp', __name__)

@receipt_settings_bp.route('/receipt-settings', methods=['GET'])
def get_settings():
    settings = db.session.query(ReceiptSettings).first()
    if not settings:
        return jsonify({
            'business_name': '',
            'header_text': '',
            'footer_text': '',
            'legal_text': '',
            'logo_filename': None
        }), 200
    return jsonify({
        'business_name': settings.business_name or '',
        'header_text': settings.header_text or '',
        'footer_text': settings.footer_text or '',
        'legal_text': settings.legal_text or '',
        'logo_filename': settings.logo_filename
    }), 200

@receipt_settings_bp.route('/receipt-settings', methods=['POST'])
@jwt_required()
@roles_required("super_admin", "admin")
def update_settings():
    data = request.json or {}
    settings = db.session.query(ReceiptSettings).first()
    if not settings:
        settings = ReceiptSettings()

    settings.business_name = data.get('business_name', '')
    settings.header_text = data.get('header_text', '')
    settings.footer_text = data.get('footer_text', '')
    settings.legal_text = data.get('legal_text', '')
    db.session.add(settings)
    db.session.commit()

    return jsonify({'message': 'Settings updated successfully'}), 200

@receipt_settings_bp.route('/receipt-settings/logo', methods=['POST'])
@jwt_required()
@roles_required("super_admin", "admin")
def upload_logo():
    # Support both 'file' and 'logo' field names for robustness
    file = request.files.get('file') or request.files.get('logo')
    if not file or file.filename == '':
        return jsonify({"error": "No file part or selected file"}), 400

    # Use absolute path
    upload_folder = os.path.join(current_app.root_path, 'static', 'receipt_logos')
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    # Save filename in DB
    settings = ReceiptSettings.query.first()
    if not settings:
        settings = ReceiptSettings()
        db.session.add(settings)

    settings.logo_filename = filename
    db.session.commit()

    return jsonify({"message": "Logo uploaded successfully", "filename": filename}), 200
