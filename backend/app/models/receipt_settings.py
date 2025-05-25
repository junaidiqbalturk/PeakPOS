# models/receipt_settings.py

from sqlalchemy import Column, Integer, String
from app import db

class ReceiptSettings(db.Model):
    __tablename__ = 'receipt_settings'

    id = Column(Integer, primary_key=True)
    business_name = Column(String(100), nullable=False)
    header_text = Column(String(255), nullable=True)
    footer_text = Column(String(255), nullable=True)
    legal_text = Column(String(255), nullable=True)
    logo_filename = Column(String(255), nullable=True)
