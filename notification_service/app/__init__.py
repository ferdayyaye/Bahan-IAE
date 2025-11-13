from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    db.init_app(app)
    ma.init_app(app)

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        from .models import Notification
        try:
            db.create_all()
            app.logger.info("Database dan tabel notifications berhasil diverifikasi/dibuat.")
        except Exception as e:
            app.logger.error(f"Gagal membuat tabel notifications: {e}")