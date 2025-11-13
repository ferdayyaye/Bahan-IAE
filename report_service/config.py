import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration"""
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==================== DATABASE ====================
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "digital_wallet")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # ==================== JWT ====================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_EXPIRES_SECONDS", "3600"))
    )

    # ==================== SERVICE-TO-SERVICE ====================
    SERVICE_TOKEN = os.getenv("SERVICE_TOKEN", "service_shared_secret_change_this")
    
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5001")
    TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL", "http://localhost:5002")

    # ==================== REPORT SERVICE ====================
    REPORT_SERVICE_PORT = int(os.getenv("REPORT_SERVICE_PORT", "5004"))
    REPORT_SERVICE_HOST = os.getenv("REPORT_SERVICE_HOST", "0.0.0.0")

    # ==================== API TIMEOUT ====================
    API_REQUEST_TIMEOUT = int(os.getenv("API_REQUEST_TIMEOUT", "5"))

    # ==================== PAGINATION ====================
    DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", "50"))
    MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", "100"))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SERVICE_TOKEN = "test-token"


# Select configuration based on FLASK_ENV
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}

Config = config.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
