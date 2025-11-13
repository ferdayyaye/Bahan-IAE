from datetime import datetime
from . import db
from .models import Report, ReportSummary
from .utils import UserServiceClient, TransactionServiceClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc

# ========== CREATE REPORT ==========
def create_report(data):
    user_id = data.get("user_id")
    transaction_id = data.get("transaction_id")
    
    if not user_id or not transaction_id:
        return None, "user_id and transaction_id are required", 400
    
    try:
        # 1. Cek apakah transaction sudah ada di report
        existing = Report.query.filter_by(transaction_id=transaction_id).first()
        if existing:
            return existing, None, 200
        
        # 2. Ambil data transaction dari transaction_service
        transaction, err = TransactionServiceClient.get_transaction(transaction_id)
        if err:
            return None, f"Transaction not found: {err}", 404
        
        # 3. Ambil data user dari user_service
        user, err = UserServiceClient.get_user(user_id)
        if err:
            return None, f"User not found: {err}", 404
        
        # 4. Create report
        report = Report(
            user_id=user_id,
            full_name=user.get("full_name"),
            email=user.get("email"),
            transaction_id=transaction_id,
            transaction_type=transaction.get("type"),
            amount=float(transaction.get("amount", 0)),
            transaction_status=transaction.get("status", "success"),
            balance_after=float(user.get("balance", 0)),
            transaction_date=datetime.fromisoformat(transaction.get("created_at")) if transaction.get("created_at") else datetime.utcnow()
        )
        
        db.session.add(report)
        db.session.commit()
        
        # 5. Update summary
        _update_summary(user_id)
        
        return report, None, 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500


# ========== GET REPORTS BY USER ==========

def get_reports_by_user(user_id, page=1, per_page=50):
    query = Report.query.filter_by(user_id=user_id).order_by(desc(Report.transaction_date))
    total = query.count()
    
    if total == 0:
        return {
            "data": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
            "total_pages": 0
        }, None, 200
    
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        "data": [r.to_dict() for r in paginated.items],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": paginated.pages
    }, None, 200


# ========== GET SUMMARY BY USER ==========
def get_summary_by_user(user_id):
    summary = ReportSummary.query.filter_by(user_id=user_id).first()
    
    if not summary:
        return None, "Summary not found", 404
    
    return summary.to_dict(), None, 200


# ========== UPDATE SUMMARY (Internal) ==========
def _update_summary(user_id):
    try:
        # 1. Ambil data user terkini
        user, err = UserServiceClient.get_user(user_id)
        if err:
            return
        
        # 2. Hitung aggregate dari reports
        reports = Report.query.filter_by(user_id=user_id).all()
        
        total_credit = sum(r.amount for r in reports if r.transaction_type == "credit")
        total_debit = sum(r.amount for r in reports if r.transaction_type == "debit")
        last_tx_date = max((r.transaction_date for r in reports), default=None) if reports else None
        
        # 3. Update atau create summary
        summary = ReportSummary.query.filter_by(user_id=user_id).first()
        
        if summary:
            summary.total_transactions = len(reports)
            summary.total_credit = total_credit
            summary.total_debit = total_debit
            summary.current_balance = float(user.get("balance", 0))
            summary.last_transaction_date = last_tx_date
        else:
            summary = ReportSummary(
                user_id=user_id,
                full_name=user.get("full_name"),
                email=user.get("email"),
                total_transactions=len(reports),
                total_credit=total_credit,
                total_debit=total_debit,
                current_balance=float(user.get("balance", 0)),
                last_transaction_date=last_tx_date
            )
            db.session.add(summary)
        
        db.session.commit()
    except Exception as e:
        print(f"Error updating summary: {str(e)}")


# ========== SYNC ALL REPORTS ==========
def sync_all_reports():
    try:
        # 1. Hapus data lama
        Report.query.delete()
        ReportSummary.query.delete()
        db.session.commit()
        
        # 2. Ambil data dari services
        transactions, err = TransactionServiceClient.get_all_transactions()
        if err:
            return None, f"Failed to fetch transactions: {err}", 500
        
        users, err = UserServiceClient.get_all_users()
        if err:
            return None, f"Failed to fetch users: {err}", 500
        
        # 3. Create user mapping untuk lookup cepat
        user_map = {u.get("id"): u for u in users}
        
        # 4. Create reports dari transactions
        count = 0
        for tx in transactions:
            user_id = tx.get("user_id")
            user = user_map.get(user_id)
            
            if user:
                report = Report(
                    user_id=user_id,
                    full_name=user.get("full_name"),
                    email=user.get("email"),
                    transaction_id=tx.get("id"),
                    transaction_type=tx.get("type"),
                    amount=float(tx.get("amount", 0)),
                    transaction_status=tx.get("status", "success"),
                    balance_after=float(user.get("balance", 0)),
                    transaction_date=datetime.fromisoformat(tx.get("created_at")) if tx.get("created_at") else datetime.utcnow()
                )
                db.session.add(report)
                count += 1
        
        db.session.commit()
        
        # 5. Rebuild summaries untuk setiap user
        for user_id in user_map.keys():
            _update_summary(user_id)
        
        return {"synced_reports": count, "synced_users": len(user_map)}, None, 200
    
    except Exception as e:
        db.session.rollback()
        return None, f"Sync error: {str(e)}", 500