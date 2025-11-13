from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    init_app(app)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=app.config["DEBUG"])