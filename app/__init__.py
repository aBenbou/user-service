import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.utils.decorators import limiter
from app.config import config
from app.log_config import configure_logging

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """Create and configure the Flask application
    
    Args:
        config_name: Name of the configuration to use
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    # Configure logging using shared log_config implementation
    configure_logging(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        """Ensure the identity is always a string (UUID is converted to string)"""
        return str(user) if user is not None else None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """We don't need to load user from database since Auth Service handles validation"""
        identity = jwt_data["sub"]
        return identity
    
    # Register blueprints
    register_blueprints(app)
    
    # Register commands
    from app.commands import init_badges
    app.cli.add_command(init_badges)
    
    # Create database tables if they don't exist
    try:
        with app.app_context():
            db.create_all()
            app.logger.info("Database tables created successfully")
    except Exception as e:
        app.logger.error(f"Error creating database tables: {str(e)}")
        app.logger.error("Application will continue startup, but database operations may fail")
    
    return app

def register_blueprints(app):
    """Register Flask blueprints
    
    Args:
        app: Flask application
    """
    # Register main blueprint for index page
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Register standard API endpoints
    from app.api.profiles import profiles_bp
    from app.api.expertise import expertise_bp
    from app.api.preferences import preferences_bp
    from app.api.connections import connections_bp
    from app.api.gamification import gamification_bp
    
    app.register_blueprint(profiles_bp, url_prefix='/api/profiles')
    app.register_blueprint(expertise_bp, url_prefix='/api')  # Routes include /profiles prefix
    app.register_blueprint(preferences_bp, url_prefix='/api')  # Routes include /profiles prefix
    app.register_blueprint(connections_bp, url_prefix='/api')  # Routes include /profiles prefix
    app.register_blueprint(gamification_bp)  # URL prefix is already set in the blueprint
