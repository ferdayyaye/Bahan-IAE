from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        """Return user data as JSON-safe dictionary"""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "balance": round(self.balance or 0.0, 2),
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }