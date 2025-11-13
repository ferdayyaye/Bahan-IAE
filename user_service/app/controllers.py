"""
controllers.py
Layer logic untuk user_service — lengkap dengan hashing password, error handling, dan CRUD aman.
"""

from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from .models import User
from . import db


# ============================================================
# CONFIGURATION & PASSWORD UTILS
# ============================================================

# Context untuk hashing password (bcrypt lebih aman)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash plain password using bcrypt."""
    if not password or len(password.strip()) == 0:
        raise ValueError("Password cannot be empty")
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify password hash safely."""
    if not password or not hashed:
        return False
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False


# ============================================================
# CORE CRUD OPERATIONS
# ============================================================

def get_all_users():
    """Return all users in database."""
    return User.query.order_by(User.id.asc()).all()


def get_user_by_id(user_id: int):
    """Return single user by ID."""
    return User.query.get(user_id)


def create_user(data: dict):
    """
    Create user (tanpa password, biasanya untuk admin).
    Fields minimal: full_name, email
    """
    if not all(k in data for k in ("full_name", "email")):
        return None, "full_name and email are required", 400

    if User.query.filter_by(email=data["email"]).first():
        return None, "Email already exists", 400

    try:
        user = User(
            full_name=data["full_name"].strip(),
            email=data["email"].strip().lower(),
            balance=float(data.get("balance", 0.0))
        )
        db.session.add(user)
        db.session.commit()
        return user, None, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500


def delete_user(user_id: int):
    """Delete a user safely."""
    user = get_user_by_id(user_id)
    if not user:
        return False, "User not found", 404

    try:
        db.session.delete(user)
        db.session.commit()
        return True, None, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", 500


# ============================================================
# AUTHENTICATION & REGISTRATION
# ============================================================

def register_user(data: dict):
    """Register new user with password hashing."""
    required = ("full_name", "email", "password")
    if not all(k in data for k in required):
        return None, "full_name, email, and password are required", 400

    # Email unique check
    email = data["email"].strip().lower()
    if User.query.filter_by(email=email).first():
        return None, "Email already exists", 400

    try:
        hashed_pw = hash_password(data["password"])
        user = User(
            full_name=data["full_name"].strip(),
            email=email,
            password_hash=hashed_pw,
            balance=0.0
        )
        db.session.add(user)
        db.session.commit()
        return user, None, 201

    except ValueError as ve:
        return None, str(ve), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500


def authenticate_user(email: str, password: str):
    """Authenticate user with email and password."""
    if not email or not password:
        return None, "Email and password are required", 400

    user = User.query.filter_by(email=email.strip().lower()).first()
    if not user or not verify_password(password, user.password_hash):
        return None, "Invalid credentials", 401

    return user, None, 200


# ============================================================
# UPDATE USER
# ============================================================

def update_user(user_id: int, data: dict, allow_balance: bool = False):
    """Update user details (balance editable only for admin/internal)."""
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404

    try:
        # Update fields
        if "full_name" in data and data["full_name"]:
            user.full_name = data["full_name"].strip()

        if "email" in data and data["email"]:
            new_email = data["email"].strip().lower()
            if User.query.filter(User.email == new_email, User.id != user_id).first():
                return None, "Email already used", 400
            user.email = new_email

        if "password" in data and data["password"]:
            user.password_hash = hash_password(data["password"])

        if "balance" in data:
            if not allow_balance:
                return None, "Not allowed to change balance here", 403
            try:
                new_balance = float(data["balance"])
                if new_balance < 0:
                    return None, "Balance cannot be negative", 400
                user.balance = new_balance
            except ValueError:
                return None, "Invalid balance value", 400

        db.session.commit()
        return user, None, 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500


# ============================================================
# BALANCE OPERATIONS
# ============================================================

def get_balance(user_id: int):
    """Return user's current balance."""
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404
    return round(user.balance or 0.0, 2), None, 200


def topup(user_id: int, amount: float):
    """Increase user balance safely."""
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return None, "Invalid amount", 400

    if amount <= 0:
        return None, "Amount must be positive", 400

    try:
        user.balance += amount
        db.session.commit()
        return user, None, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500


def debit(user_id: int, amount: float):
    """Decrease user balance safely."""
    user = get_user_by_id(user_id)
    if not user:
        return None, "User not found", 404

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return None, "Invalid amount", 400

    if amount <= 0:
        return None, "Amount must be positive", 400

    if user.balance < amount:
        return None, "Insufficient balance", 402

    try:
        user.balance -= amount
        db.session.commit()
        return user, None, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}", 500