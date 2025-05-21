import os
from datetime import timedelta

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _get_int_env(var_name: str, default: int) -> int:
    """Return an int from env or fall back to *default*.

    The helper is defensive: it allows comments or extra whitespace in the
    variable (e.g. "3600  # 1 hour") and silently falls back to *default* if
    conversion fails.
    """
    raw = os.getenv(var_name)
    if raw is None:
        return default

    # Take only the first numeric token to ignore inline comments.
    token = raw.strip().split()[0]
    try:
        return int(token)
    except (TypeError, ValueError):
        return default

class Config:
    """Base configuration."""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///auth.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = _get_int_env('REDIS_PORT', 6379)
    REDIS_DB = _get_int_env('REDIS_DB', 0)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() in ('true', '1', 't')
    RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '60/minute')
    RATE_LIMIT_STORAGE_URL = os.getenv('RATE_LIMIT_STORAGE_URL', 'redis://localhost:6379/0')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=_get_int_env('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=_get_int_env('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    JWT_TOKEN_LOCATION = ['headers']
    
    # Auth Service
    AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth_api:5000')
    AUTH_SERVICE_TOKEN = os.getenv('AUTH_SERVICE_TOKEN', 'placeholder-token')
    
    # Event Bus
    EVENT_BUS_ENABLED = os.getenv('EVENT_BUS_ENABLED', 'False').lower() in ('true', '1', 't')
    EVENT_BUS_TYPE = os.getenv('EVENT_BUS_TYPE', 'http')
    EVENT_BUS_URL = os.getenv('EVENT_BUS_URL', 'http://event_bus:8080/events')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RATE_LIMIT_ENABLED = False
    JWT_SECRET_KEY = 'test-jwt-key'
    AUTH_SERVICE_URL = 'http://localhost:5000'
    EVENT_BUS_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # Override these with environment variables in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# Config dictionary to map environment names to config classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}