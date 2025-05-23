from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship("Product", back_populates="category", cascade="all, delete-orphan")
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
