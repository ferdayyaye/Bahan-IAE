# Initialize Flask app and extensions
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

# Inisialisasi ekstensi global
db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    # Inisialisasi ekstensi
    db.init_app(app)
    ma.init_app(app)
    CORS(app)

    # Import model agar dikenali SQLAlchemy
    from . import models  # noqa: F401

    # Registrasi semua routes (Blueprint)
    from .routes import register_routes
    register_routes(app)

    # Buat tabel di database jika belum ada
    with app.app_context():
        db.create_all()
