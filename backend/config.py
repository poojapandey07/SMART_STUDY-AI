import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    """Production-ready configuration settings for SmartStudy AI Flask app."""
    
    # Environment & Debug
    ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    PORT = int(os.getenv('PORT', 5000))
    
    # Security Secrets
    SECRET_KEY = os.getenv('SECRET_KEY', 'smartstudy-default-secret-key-2026')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'smartstudy-default-jwt-key-2026')
    
    # JWT Expiration
    jwt_days = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES_DAYS', 7))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=jwt_days)
    JWT_HEADER_TYPE = 'Bearer'
    
    # Database Configuration (SQLite default with absolute path)
    db_url = os.getenv('DATABASE_URL', 'sqlite:///smartstudy.db')
    if db_url.startswith('sqlite:///'):
        db_path = db_url.replace('sqlite:///', '')
        if not os.path.isabs(db_path):
            db_path = os.path.join(BASE_DIR, db_path)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    else:
        SQLALCHEMY_DATABASE_URI = db_url
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Engine Configuration
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'mock').lower() # gemini, openai, mock
    AI_MODEL = os.getenv('AI_MODEL', 'gemini-1.5-flash')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
