from flask import Blueprint, request, jsonify
from .controllers import (
    create_transaction,
    get_all_transactions,
    get_transaction_by_id,
    update_transaction_status,
    delete_transaction,
    get_transactions_by_user,
)
from .schemas import transaction_schema, transactions_schema

bp = Blueprint("tx_bp", __name__, url_prefix="/transactions")

# =====================================================
# ✅ CREATE TRANSACTION
# =====================================================
@bp.route("", methods=["POST"])
def create_tx_route():
    payload = request.get_json(silent=True) or {}
    errors = transaction_schema.validate(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    tx, err, status = create_transaction(payload)
    if err:
        return jsonify({"error": err}), status

    return transaction_schema.jsonify(tx), status


# =====================================================
# ✅ GET ALL TRANSACTIONS
# =====================================================
@bp.route("", methods=["GET"])
def list_txs():
    txs = get_all_transactions()
    return transactions_schema.jsonify(txs), 200


# =====================================================
# ✅ GET SINGLE TRANSACTION
# =====================================================
@bp.route("/<int:tx_id>", methods=["GET"])
def get_tx(tx_id):
    tx = get_transaction_by_id(tx_id)
    if not tx:
        return jsonify({"error": "Transaction not found"}), 404
    return transaction_schema.jsonify(tx), 200


# =====================================================
# ✅ UPDATE TRANSACTION STATUS
# =====================================================
@bp.route("/<int:tx_id>", methods=["PUT"])
def update_tx(tx_id):
    payload = request.get_json(silent=True) or {}
    status = payload.get("status")

    if not status:
        return jsonify({"error": "status required"}), 400

    tx, err, st = update_transaction_status(tx_id, status)
    if err:
        return jsonify({"error": err}), st

    return transaction_schema.jsonify(tx), st


# =====================================================
# ✅ DELETE TRANSACTION
# =====================================================
@bp.route("/<int:tx_id>", methods=["DELETE"])
def delete_tx(tx_id):
    ok, err, st = delete_transaction(tx_id)
    if err:
        return jsonify({"error": err}), st
    return jsonify({"message": "Transaction deleted"}), 200


# =====================================================
# ✅ GET TRANSACTIONS BY USER (External API)
# =====================================================
@bp.route("/user/<int:user_id>", methods=["GET"])
def get_txs_by_user(user_id):
    txs = get_transactions_by_user(user_id)
    if not txs:
        return jsonify([]), 200
    return transactions_schema.jsonify(txs), 200


# =====================================================
# ✅ INTERNAL ENDPOINT (Frontend Dashboard)
# =====================================================
@bp.route("/internal/user/<int:user_id>", methods=["GET"])
def internal_get_txs_by_user(user_id):
    """
    Endpoint internal untuk frontend.
    Mengambil transaksi berdasarkan user_id secara efisien.
    Tidak berat karena hanya query user_id & urut DESC by created_at.
    """
    try:
        txs = get_transactions_by_user(user_id)
        data = transactions_schema.dump(txs)
        return jsonify(data), 200
    except Exception as e:
        print(f"[ERROR] internal_get_txs_by_user: {e}")
        return jsonify({"error": "Failed to fetch transactions"}), 500


# REGISTER BLUEPRINT
def register_routes(app):
    app.register_blueprint(bp)