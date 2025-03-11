from app import db
from app.models.category import Category  # Ensure Category is imported first


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id', name="fk_product_category"),  #Explicitly name the foreign key
        nullable=False
    )
    image_url = db.Column(db.String(255), nullable=True)

    category = db.relationship("Category", back_populates="products")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "image_url": self.image_url
        }
