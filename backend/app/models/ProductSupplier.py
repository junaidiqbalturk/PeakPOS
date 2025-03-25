from app import db
from datetime import datetime


class ProductSupplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at which the supplier sells the product
    supply_date = db.Column(db.DateTime, default=datetime.utcnow)  # Last supplied date

    product = db.relationship("Product", back_populates="supplier_associations")
    supplier = db.relationship("Supplier", back_populates="product_associations")

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_id": self.supplier_id,
            "product_id": self.product_id,
            "price": self.price,
            "supply_date": self.supply_date.strftime("%Y-%m-%d %H:%M:%S")
        }
