from app import db
from datetime import datetime


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)  # Action performed
    details = db.Column(db.Text, nullable=True)  # Additional details (e.g., changed values)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # When the action occurred

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "details": self.details,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }


def log_activity(user_id, action, details=None):
    """Log user actions into the ActivityLog table"""
    log_entry = ActivityLog(user_id=user_id, action=action, details=details)
    db.session.add(log_entry)
    db.session.commit()
