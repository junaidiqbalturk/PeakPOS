from app import db
from app.models.category import Category  # Ensure Category is imported first


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(100), nullable=True, index=True)
    price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', name="fk_product_category"),  #Explicitly name the foreign key
        nullable=False
    )
    image_url = db.Column(db.String(255), nullable=True)

    # Relationship
    tenant = db.relationship("Tenant", back_populates="products")
    category = db.relationship("Category", back_populates="products")
    supplier_associations = db.relationship("ProductSupplier", back_populates="product", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "barcode": self.barcode,
            "price": self.price,
            "cost_price": self.cost_price,
            "stock": self.stock,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "image_url": self.image_url,
            "suppliers": [assoc.to_dict() for assoc in self.supplier_associations]
        }
