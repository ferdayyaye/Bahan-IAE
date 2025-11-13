from flask import Blueprint, request, jsonify
from .controllers import (
    create_report,
    get_reports_by_user,
    get_summary_by_user,
    sync_all_reports
)

# Blueprints
bp = Blueprint("reports", __name__, url_prefix="/reports")
summary_bp = Blueprint("summaries", __name__, url_prefix="/summaries")
sync_bp = Blueprint("sync", __name__, url_prefix="/sync")

# =============== REPORT ROUTES =======================
@bp.route("", methods=["POST"])
def create_report_route():
    payload = request.get_json() or {}
    if "user_id" not in payload or "transaction_id" not in payload:
        return jsonify({"error": "user_id and transaction_id are required"}), 400

    report, err, status = create_report(payload)
    if err:
        return jsonify({"error": err}), status
    return jsonify(report.to_dict()), status


@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_reports(user_id):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)
    data, err, status = get_reports_by_user(user_id, page=page, per_page=per_page)
    if err:
        return jsonify({"error": err}), status
    return jsonify(data), status


@summary_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_summary(user_id):
    data, err, status = get_summary_by_user(user_id)
    if err:
        return jsonify({"error": err}), status
    return jsonify(data), status


# =============== SYNC ROUTES =========================
@sync_bp.route("/all", methods=["POST"])
def sync_reports_route():
    result, err, status = sync_all_reports()
    if err:
        return jsonify({"error": err}), status
    return jsonify(result), status


# =============== REGISTER ALL BLUEPRINTS ==============
def register_routes(app):
    app.register_blueprint(bp)
    app.register_blueprint(summary_bp)
    app.register_blueprint(sync_bp)