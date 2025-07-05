import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Set Flask configuration from environment variables."""

    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-that-is-not-secure'
    FLASK_APP = os.environ.get('FLASK_APP') or 'run.py'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 