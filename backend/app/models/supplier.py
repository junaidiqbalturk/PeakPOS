from app import db
from datetime import datetime


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship: One supplier can provide multiple products
    product_associations = db.relationship("ProductSupplier", back_populates="supplier", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert supplier object to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "contact": self.contact,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            # Include products in response (Optional)
            "products": [product.to_dict() for product in self.products]
        }
