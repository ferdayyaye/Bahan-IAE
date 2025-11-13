from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# ============================
# Konfigurasi service
# ============================
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5001")
TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL", "http://localhost:5002")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:5003")
REPORT_SERVICE_URL = os.getenv("REPORT_SERVICE_URL", "http://localhost:5004")

SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "service_shared_secret_change_this")


# ============================
# Helper function
# ============================
def forward_request(base_url):
    """Meneruskan request ke service terkait"""
    path = request.path
    method = request.method
    headers = {}

    # Forward Authorization header jika ada
    auth_header = request.headers.get("Authorization")
    if auth_header:
        headers["Authorization"] = auth_header

    # Tambahkan service token internal
    headers["X-Service-Token"] = SERVICE_TOKEN

    url = f"{base_url}{path}"
    try:
        data = request.get_json(silent=True)
        if method == "GET":
            resp = requests.get(url, headers=headers, params=request.args, timeout=20)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=20)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=data, timeout=20)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=20)
        else:
            return jsonify({"error": "Unsupported method"}), 405

        # Return response JSON ke frontend
        return jsonify(resp.json()), resp.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": f"Service at {base_url} unavailable"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================
# ROUTES ke masing-masing service
# ============================

@app.route("/auth/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/users", methods=["GET", "POST"])
@app.route("/users/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def user_routes(path=None):
    return forward_request(USER_SERVICE_URL)

@app.route("/transactions", methods=["GET", "POST"])
@app.route("/transactions/<path:path>", methods=["GET", "PUT", "DELETE"])
def transaction_routes(path=None):
    return forward_request(TRANSACTION_SERVICE_URL)

@app.route("/notifications", methods=["GET", "POST"])
@app.route("/notifications/<path:path>", methods=["GET", "DELETE"])
def notification_routes(path=None):
    return forward_request(NOTIFICATION_SERVICE_URL)

@app.route("/reports", methods=["GET", "POST"])
@app.route("/reports/<path:path>", methods=["GET", "DELETE"])
def report_routes(path=None):
    return forward_request(REPORT_SERVICE_URL)

@app.route("/sync", methods=["GET", "POST"])
@app.route("/sync/<path:path>", methods=["GET", "POST"])
def sync_routes(path=None):
    return forward_request(REPORT_SERVICE_URL)

@app.route("/")
def home():
    return jsonify({
        "message": "API Gateway running 🚀",
        "routes": [
            "/auth/*",
            "/users/*",
            "/transactions/*",
            "/notifications/*",
            "/reports/*"
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)