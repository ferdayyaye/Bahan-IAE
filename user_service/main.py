from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app import init_app

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint tidak ditemukan"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Terjadi kesalahan di server"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=app.config.get("DEBUG", True)
    )
