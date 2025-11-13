from flask import Flask
from flask_cors import CORS
from config import Config
from app import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_app(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=app.config["DEBUG"])