from flask import Blueprint, request, jsonify
from .controllers import (
    create_notification, get_all_notifications,
    get_notification_by_id, send_notification_email
)
from .schemas import notification_schema, notifications_schema
from .models import Notification
from . import db

bp = Blueprint("notif_bp", __name__, url_prefix="/notifications")

# CREATE
@bp.route("", methods=["POST"])
def create_notif():
    payload = request.get_json() or {}
    if "user_id" not in payload or "message" not in payload:
        return jsonify({"error": "user_id and message are required"}), 400
    notif, err, status = create_notification(payload)
    return notification_schema.jsonify(notif), status


# READ (ALL)
@bp.route("", methods=["GET"])
def list_notifs():
    notifs = get_all_notifications()
    return notifications_schema.jsonify(notifs), 200


# READ (BY ID)
@bp.route("/<int:notif_id>", methods=["GET"])
def get_notif(notif_id):
    notif = get_notification_by_id(notif_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404
    return notification_schema.jsonify(notif), 200


# UPDATE
@bp.route("/<int:notif_id>", methods=["PUT"])
def update_notif(notif_id):
    notif = get_notification_by_id(notif_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404

    payload = request.get_json() or {}
    notif.message = payload.get("message", notif.message)
    notif.status = payload.get("status", notif.status)
    db.session.commit()

    return notification_schema.jsonify(notif), 200


# DELETE
@bp.route("/<int:notif_id>", methods=["DELETE"])
def delete_notif(notif_id):
    notif = get_notification_by_id(notif_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404
    db.session.delete(notif)
    db.session.commit()
    return jsonify({"message": "Notification deleted"}), 200


# SEND
@bp.route("/<int:notif_id>/send", methods=["POST"])
def send_notif(notif_id):
    notif = get_notification_by_id(notif_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404
    ok, err = send_notification_email(notif)
    if not ok:
        return jsonify({"error": err}), 500
    return jsonify({"message": "Notification sent", "status": notif.status}), 200


# RESEND
@bp.route("/<int:notif_id>/resend", methods=["POST"])
def resend_notif(notif_id):
    notif = get_notification_by_id(notif_id)
    if not notif:
        return jsonify({"error": "Notification not found"}), 404

    if notif.status != "failed":
        return jsonify({"error": "Only failed notifications can be resent"}), 400

    ok, err = send_notification_email(notif)
    if not ok:
        return jsonify({"error": err}), 500
    return jsonify({"message": "Notification resent", "status": notif.status}), 200



def register_routes(app):
    app.register_blueprint(bp)