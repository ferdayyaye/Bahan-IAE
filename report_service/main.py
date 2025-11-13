from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from app import init_app

def create_app():
    app = Flask(__name__)
    
    # Load konfigurasi dari class Config (config.py)
    app.config.from_object(Config)
    
    # Inisialisasi semua ekstensi & route dari app/__init__.py
    init_app(app)
    
    # Aktifkan CORS untuk akses dari domain lain (misal frontend)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Penanganan error umum agar respons selalu JSON
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint tidak ditemukan"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Terjadi kesalahan di server"}), 500
    
    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "OK", "service": "report-service"}), 200
    
    return app


# Inisialisasi aplikasi
app = create_app()


if __name__ == "__main__":
    # Jalankan server di port 5004
    app.run(
        host="0.0.0.0",
        port=5004,
        debug=app.config.get("DEBUG", True)
    )
