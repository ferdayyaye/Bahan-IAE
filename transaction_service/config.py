import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "digital_wallet_users")

    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5001")
    NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:5003")


    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "service_shared_secret_change_this")
