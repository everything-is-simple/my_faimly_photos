from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    """Creates and configures an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # The following needs to be imported here to avoid circular imports
    with app.app_context():
        from . import models

        # Register blueprints
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp)
        
        return app 