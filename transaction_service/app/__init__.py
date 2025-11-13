from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    from .routes import register_routes
    register_routes(app)