from app import db
from datetime import datetime


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    discount_type = db.Column(db.String(20), nullable=False)  # 'percentage' or 'fixed'
    value = db.Column(db.Float, nullable=False)  # Discount value
    active = db.Column(db.Boolean, default=True)  # Is the discount active?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert Discount object to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "discount_type": self.discount_type,
            "value": self.value,
            "active": self.active,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
