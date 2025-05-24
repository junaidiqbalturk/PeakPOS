from datetime import datetime
from app import db #SQL Alchmey instance

class Receipt(db.Model):
    __tablename__ = 'receipts'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #JSON snapshot of the receipt
    snapshot = db.Column(db.JSON, nullable=False)

    # Link to PDF for later generation
    pdf_url = db.Column(db.String(255), nullable=True)

    order = db.relationship('Order', back_populates='receipts')
    user = db.relationship("User", back_populates="receipts")
