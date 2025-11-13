from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from .models import User
from . import db

# ======================================================
# Blueprints
# ======================================================
bp = Blueprint("user_bp", __name__, url_prefix="/users")
auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")
internal_bp = Blueprint("internal_user_bp", __name__, url_prefix="/internal/users")

# ======================================================
# AUTH ROUTES
# ======================================================
@auth_bp.route("/register", methods=["POST"])
def register_route():
    """User registration"""
    data = request.get_json() or {}
    required = ("full_name", "email", "password")

    if not all(data.get(k) for k in required):
        return jsonify({"error": "full_name, email, and password are required"}), 400

    if User.query.filter_by(email=data["email"].lower().strip()).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        new_user = User(
            full_name=data["full_name"].strip(),
            email=data["email"].strip().lower(),
            password_hash=generate_password_hash(data["password"]),
            role=data.get("role", "user")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success": True, "user": new_user.to_dict()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """User login"""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
        "success": True
    }), 200

# ======================================================
# USER CRUD ROUTES
# ======================================================
@bp.route("", methods=["POST"])
@jwt_required(optional=True)
def create_user_route():
    """Admin can create new user"""
    data = request.get_json() or {}
    required = ("full_name", "email", "password")

    if not all(data.get(k) for k in required):
        return jsonify({"error": "full_name, email, and password are required"}), 400

    # Cek duplikat email
    if User.query.filter_by(email=data["email"].lower().strip()).first():
        return jsonify({"error": "Email already registered"}), 400

    try:
        # Buat user baru
        new_user = User(
            full_name=data["full_name"].strip(),
            email=data["email"].strip().lower(),
            password_hash=generate_password_hash(data["password"]),
            role=data.get("role", "user")
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "User added successfully",
            "user": new_user.to_dict()
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("", methods=["GET"])
@jwt_required(optional=True)
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@bp.route("/<int:user_id>", methods=["GET"])
@jwt_required(optional=True)
def get_user_route(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@bp.route("/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_route(user_id):
    """Update user details"""
    current_id = int(get_jwt_identity())
    current = User.query.get(current_id)
    if not current:
        return jsonify({"error": "Unauthorized"}), 403

    # Admin can edit anyone, users can only edit themselves
    if current.role != "admin" and current_id != user_id:
        return jsonify({"error": "Permission denied"}), 403

    data = request.get_json() or {}
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        if "full_name" in data:
            user.full_name = data["full_name"].strip()
        if "email" in data:
            new_email = data["email"].strip().lower()
            if User.query.filter(User.email == new_email, User.id != user_id).first():
                return jsonify({"error": "Email already in use"}), 400
            user.email = new_email
        if "password" in data and data["password"]:
            user.password_hash = generate_password_hash(data["password"])
        if "role" in data and current.role == "admin":
            user.role = data["role"]
        if "balance" in data and current.role == "admin":
            user.balance = float(data["balance"])

        db.session.commit()
        return jsonify({"success": True, "user": user.to_dict()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_route(user_id):
    current = User.query.get(int(get_jwt_identity()))
    if not current or current.role != "admin":
        return jsonify({"error": "Admin only"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully", "success": True}), 200

# ======================================================
# BALANCE ROUTES
# ======================================================
@bp.route("/<int:user_id>/balance", methods=["GET"])
@jwt_required(optional=True)
def get_balance_route(user_id):
    """
    Get user's balance.
    Jika Authorization header tidak dikirim, tetap diizinkan untuk testing manual.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"success": True, "user_id": user.id, "balance": user.balance}), 200


@bp.route("/<int:user_id>/topup", methods=["POST"])
@jwt_required()
def topup_route(user_id):
    """Top-up user balance"""
    current_id = int(get_jwt_identity())
    current = User.query.get(current_id)
    if not current:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    try:
        amount = float(data.get("amount", 0))
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400
    except ValueError:
        return jsonify({"error": "Amount must be numeric"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.balance += amount
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Top-up of Rp {amount:,.0f} successful.",
        "balance": user.balance
    }), 200


@bp.route("/<int:user_id>/debit", methods=["POST"])
@jwt_required()
def debit_route(user_id):
    """Reduce user balance"""
    current_id = int(get_jwt_identity())
    current = User.query.get(current_id)
    if not current:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    try:
        amount = float(data.get("amount", 0))
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400
    except ValueError:
        return jsonify({"error": "Amount must be numeric"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    user.balance -= amount
    db.session.commit()
    return jsonify({
        "success": True,
        "message": f"Rp {amount:,.0f} has been deducted.",
        "balance": user.balance
    }), 200

# ======================================================
# INTERNAL SERVICE ENDPOINTS
# ======================================================
@internal_bp.route("/<int:user_id>", methods=["GET"])
def internal_get_user(user_id):
    token = request.headers.get("X-Service-Token")
    if token != current_app.config.get("SERVICE_TOKEN"):
        return jsonify({"error": "Unauthorized"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@internal_bp.route("/<int:user_id>/balance", methods=["PUT"])
def internal_update_balance(user_id):
    token = request.headers.get("X-Service-Token")
    if token != current_app.config.get("SERVICE_TOKEN"):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    action = data.get("action")
    try:
        amount = float(data.get("amount", 0))
    except ValueError:
        return jsonify({"error": "Amount must be numeric"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if action == "credit":
        user.balance += amount
    elif action == "debit":
        if user.balance < amount:
            return jsonify({"error": "Insufficient balance"}), 400
        user.balance -= amount
    else:
        return jsonify({"error": "Invalid action"}), 400

    db.session.commit()
    return jsonify({"success": True, "user": user.to_dict()}), 200

# ======================================================
# REGISTER BLUEPRINTS
# ======================================================
def register_routes(app):
    app.register_blueprint(bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(internal_bp)