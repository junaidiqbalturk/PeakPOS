import os
from pathlib import Path

# Load .env file if python-dotenv is installed and .env exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")

    # Database configuration with environment variable support
    DB_USER = os.getenv("DB_USER", "peakpos_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "greamesmith")
    DB_HOST = os.getenv("DB_HOST", "localhost\\SQLEXPRESS")
    DB_NAME = os.getenv("DB_NAME", "PeakPOS")
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC+Driver+18+for+SQL+Server")

    DEFAULT_DB_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        f"?driver={DB_DRIVER}&TrustServerCertificate=yes"
    )

    # Use SQLite file fallback if SQL Server is not reachable and SQLALCHEMY_DATABASE_URI is not set
    sqlite_fallback_path = (Path(__file__).resolve().parent / "instance" / "peakpos.db").as_posix()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not SQLALCHEMY_DATABASE_URI:
        # Check if MSSQL is reachable or default to SQLite fallback
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", DEFAULT_DB_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
