from app import db
from datetime import datetime

class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    return_id = db.Column(db.Integer, db.ForeignKey('return.id'), nullable=False, unique=True)  # ✅ Link to Returns
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ✅ Who gets the refund
    refund_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # ✅ Can be 'Pending' or 'Completed'
    refund_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "return_id": self.return_id,
            "user_id": self.user_id,
            "refund_amount": self.refund_amount,
            "status": self.status,
            "refund_date": self.refund_date.strftime("%Y-%m-%d %H:%M:%S")
        }
