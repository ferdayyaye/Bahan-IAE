from datetime import datetime
from . import db

class Report(db.Model):
    __tablename__ = "reports"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # User Information
    user_id = db.Column(db.Integer, nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    # Transaction Information
    transaction_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    transaction_type = db.Column(db.String(20), nullable=False)  # debit | credit
    amount = db.Column(db.Float, nullable=False)
    transaction_status = db.Column(db.String(20), default="success")
    
    # Balance snapshot saat transaksi
    balance_after = db.Column(db.Float, nullable=True)
    
    # Timestamps
    transaction_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_user_tx', 'user_id', 'transaction_id'),
        db.Index('idx_user_date', 'user_id', 'transaction_date'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "type": self.transaction_type,
            "amount": round(self.amount, 2),
            "status": self.transaction_status,
            "balance_after": round(self.balance_after or 0.0, 2),
            "transaction_date": self.transaction_date.isoformat(),
            "created_at": self.created_at.isoformat()
        }


class ReportSummary(db.Model):
    __tablename__ = "report_summaries"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, unique=True, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    
    total_transactions = db.Column(db.Integer, default=0)
    total_credit = db.Column(db.Float, default=0.0)  # topup
    total_debit = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    
    last_transaction_date = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Return summary data as JSON"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "total_transactions": self.total_transactions,
            "total_credit": round(self.total_credit, 2),
            "total_debit": round(self.total_debit, 2),
            "current_balance": round(self.current_balance, 2),
            "last_transaction_date": self.last_transaction_date.isoformat() if self.last_transaction_date else None,
            "updated_at": self.updated_at.isoformat()
        }
