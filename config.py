import os

class Config:
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Usage in your Flask app:
# from config import Config
# app.config.from_object(Config)