# routes/receipt_settings.py

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from app import db, app
import logging
from app.models.receipt_settings import ReceiptSettings

receipt_settings_bp = Blueprint('receipt_settings_bp', __name__)
# UPLOAD_FOLDER = 'static/receipt_logos'

@receipt_settings_bp.route('/receipt-settings', methods=['GET'])
def get_settings():
    settings = db.session.query(ReceiptSettings).first()
    if not settings:
        return jsonify({}), 404
    return jsonify({
        'business_name': settings.business_name,
        'header_text': settings.header_text,
        'footer_text': settings.footer_text,
        'legal_text': settings.legal_text,
        'logo_filename': settings.logo_filename
    })

@receipt_settings_bp.route('/receipt-settings', methods=['POST'])
def update_settings():
    data = request.json
    settings = db.session.query(ReceiptSettings).first()
    if not settings:
        settings = ReceiptSettings()

    settings.business_name = data.get('business_name', '')
    settings.header_text = data.get('header_text', '')
    settings.footer_text = data.get('footer_text', '')
    settings.legal_text = data.get('legal_text', '')
    db.session.add(settings)
    db.session.commit()

    return jsonify({'message': 'Settings updated successfully'})

@receipt_settings_bp.route('/receipt-settings/logo', methods=['POST'])
def upload_logo():
    if 'file' not in request.files:
        logging.basicConfig(level=logging.DEBUG)
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        logging.basicConfig(level=logging.DEBUG)
        return jsonify({"error": "No selected file"}), 400

    # Use absolute path
    upload_folder = os.path.join(current_app.root_path, 'static', 'receipt_logos')
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    # ✅ Save filename in DB
    settings = ReceiptSettings.query.first()
    if not settings:
        settings = ReceiptSettings()
        db.session.add(settings)

    settings.logo_filename = filename
    db.session.commit()

    return jsonify({"message": "Logo uploaded successfully", "filename": filename}), 200