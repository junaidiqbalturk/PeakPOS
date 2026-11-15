from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True, index=True)
    name = db.Column(db.String(100), nullable=False)

    tenant = db.relationship("Tenant", back_populates="categories")
    products = db.relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name
        }
