from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def init_app(app):
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from . import models

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()