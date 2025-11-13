import threading
import requests
from flask import current_app
from .models import Transaction
from . import db

# =========================================================
# CREATE TRANSACTION (versi cepat, aman, tanpa timeout)
# =========================================================
def create_transaction(data):
    """
    Buat transaksi baru, validasi user, update saldo lewat user_service,
    dan kirim notifikasi ke notification_service (non-blocking).
    """
    user_service = current_app.config["USER_SERVICE_URL"]
    notif_service = current_app.config["NOTIFICATION_SERVICE_URL"]
    service_token = current_app.config.get("SERVICE_TOKEN")

    user_id = data.get("user_id")
    tx_type = data.get("type", "debit")
    amount = float(data.get("amount", 0))

    if not user_id or amount <= 0:
        return None, "Invalid user_id or amount", 400

    headers = {"X-Service-Token": service_token}

    # 1️⃣ Pastikan user valid (timeout singkat biar cepat gagal)
    try:
        user_resp = requests.get(
            f"{user_service}/internal/users/{user_id}",
            headers=headers,
            timeout=5
        )
        if user_resp.status_code != 200:
            return None, "User not found", 404
    except requests.exceptions.RequestException:
        return None, "User service unreachable", 503

    # 2️⃣ Simpan transaksi dulu (biar frontend langsung dapat respons)
    tx = Transaction(user_id=user_id, type=tx_type, amount=amount, status="pending")
    db.session.add(tx)
    db.session.commit()

    # 3️⃣ Jalankan update saldo dan notifikasi di background thread
    def background_process():
        """Update saldo & kirim notifikasi tanpa blokir request utama."""
        try:
            # Update saldo user
            action = "credit" if tx_type == "credit" else "debit"
            payload = {"action": action, "amount": amount}
            upd = requests.put(
                f"{user_service}/internal/users/{user_id}/balance",
                json=payload,
                headers=headers,
                timeout=10
            )

            if upd.status_code == 200:
                tx.status = "success"
            else:
                tx.status = "failed"

        except Exception as e:
            tx.status = "failed"
            print(f"[WARN] Gagal update saldo user: {e}")

        # Kirim notifikasi ke notification_service
        try:
            action_text = "Top-up" if tx_type == "credit" else "Debit"
            message = f"{action_text} sebesar Rp {amount:,.0f} berhasil dilakukan."
            notify_notification_service(user_id, message)
        except Exception as e:
            print(f"[WARN] Gagal kirim notifikasi: {e}")

        # Commit hasil update status
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR] Gagal commit transaksi: {e}")

    threading.Thread(target=background_process, daemon=True).start()

    # 4️⃣ Kembalikan respons instan
    return tx, None, 201


# =========================================================
# NOTIFICATION HELPER
# =========================================================
def notify_notification_service(user_id, message):
    """Kirim notifikasi ke notification_service."""
    try:
        headers = {"X-Service-Token": current_app.config["SERVICE_TOKEN"]}
        payload = {"user_id": user_id, "message": message}
        url = f"{current_app.config['NOTIFICATION_SERVICE_URL']}/notifications"

        res = requests.post(url, json=payload, headers=headers, timeout=5)
        if res.status_code == 201:
            return True, None
        return False, res.text
    except Exception as e:
        print(f"[WARN] Gagal kirim notifikasi: {e}")
        return False, str(e)


# =========================================================
# TRANSACTION CRUD FUNCTIONS
# =========================================================
def get_all_transactions():
    """Ambil semua transaksi (urut terbaru)."""
    return Transaction.query.order_by(Transaction.created_at.desc()).all()


def get_transaction_by_id(tx_id):
    """Ambil 1 transaksi berdasarkan ID."""
    return Transaction.query.get(tx_id)


def update_transaction_status(tx_id, status):
    """Ubah status transaksi."""
    tx = get_transaction_by_id(tx_id)
    if not tx:
        return None, "Transaction not found", 404
    tx.status = status
    db.session.commit()
    return tx, None, 200


def delete_transaction(tx_id):
    """Hapus transaksi."""
    tx = get_transaction_by_id(tx_id)
    if not tx:
        return False, "Transaction not found", 404
    db.session.delete(tx)
    db.session.commit()
    return True, None, 200


def get_transactions_by_user(user_id):
    """Ambil transaksi berdasarkan user tertentu."""
    return (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )