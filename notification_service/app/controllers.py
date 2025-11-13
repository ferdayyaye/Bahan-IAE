from .models import Notification
from . import db
import smtplib
from email.mime.text import MIMEText
from flask import current_app

def create_notification(payload):
    notif = Notification(**payload)
    db.session.add(notif)
    db.session.commit()
    return notif, None, 201

def get_all_notifications():
    return Notification.query.all()

def get_notification_by_id(nid):
    return Notification.query.get(nid)

def send_notification_email(notification):
    """Mengirim email ke user berdasarkan data dari user_service"""
    try:
        # Ambil data user dari user_service
        import requests
        headers = {"X-Service-Token": current_app.config["SERVICE_TOKEN"]}
        res = requests.get(
            f"{current_app.config['USER_SERVICE_URL']}/internal/users/{notification.user_id}",
            headers=headers
        )
        if res.status_code != 200:
            notification.status = "failed"
            db.session.commit()
            return False, "User not found"

        user = res.json()
        recipient = user.get("email")

        # Kirim email
        msg = MIMEText(notification.message)
        msg["Subject"] = "Digital Wallet Notification"
        msg["From"] = current_app.config["SMTP_USER"]
        msg["To"] = recipient

        with smtplib.SMTP(current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]) as server:
            server.starttls()
            server.login(current_app.config["SMTP_USER"], current_app.config["SMTP_PASS"])
            server.send_message(msg)

        notification.status = "sent"
        db.session.commit()
        return True, None

    except Exception as e:
        notification.status = "failed"
        db.session.commit()
        return False, str(e)
