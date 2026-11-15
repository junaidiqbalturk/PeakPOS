from app import db
from datetime import datetime


class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    business_type = db.Column(db.String(50), default="retail")  # retail, pharmacy, grocery, boutique, etc.
    currency = db.Column(db.String(10), default="USD")
    tax_rate = db.Column(db.Float, default=7.0)
    plan = db.Column(db.String(30), default="starter")          # starter, professional, enterprise
    status = db.Column(db.String(20), default="active")         # active, trial, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    users = db.relationship('User', back_populates='tenant', cascade='all, delete-orphan')
    products = db.relationship('Product', back_populates='tenant', cascade='all, delete-orphan')
    categories = db.relationship('Category', back_populates='tenant', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='tenant', cascade='all, delete-orphan')
    branches = db.relationship('TenantBranch', back_populates='tenant', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "business_type": self.business_type,
            "currency": self.currency,
            "tax_rate": self.tax_rate,
            "plan": self.plan,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class TenantBranch(db.Model):
    __tablename__ = 'tenant_branches'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    is_main = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tenant = db.relationship('Tenant', back_populates='branches')

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "code": self.code,
            "address": self.address,
            "is_main": self.is_main
        }
