from app import db
from datetime import datetime


class InventoryAdjustment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)  # Only admins can adjust stock
    adjustment_type = db.Column(db.String(20), nullable=False)  # Increase or Decrease
    quantity_changed = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)  # Reason for adjustment
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="adjustments")
    admin = db.relationship("User", backref="adjustments")  # Track which admin made the change
