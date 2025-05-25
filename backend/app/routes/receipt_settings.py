# routes/receipt_settings.py

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db
from models.receipt_settings import ReceiptSettings

receipt_settings_bp = Blueprint('receipt_settings_bp', __name__)
UPLOAD_FOLDER = 'static/receipt_logos/'

@receipt_settings_bp.route('/api/receipt-settings', methods=['GET'])
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

@receipt_settings_bp.route('/api/receipt-settings', methods=['POST'])
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

@receipt_settings_bp.route('/api/receipt-settings/logo', methods=['POST'])
def upload_logo():
    file = request.files['logo']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        settings = db.session.query(ReceiptSettings).first()
        if not settings:
            settings = ReceiptSettings()

        settings.logo_filename = filename
        db.session.add(settings)
        db.session.commit()

        return jsonify({'message': 'Logo uploaded successfully', 'filename': filename})
    return jsonify({'error': 'No file uploaded'}), 400
