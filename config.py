import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'unknown-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:adminSecret@localhost:5432/flask-by-example')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 0)
    APP_SETTINGS = os.getenv('APP_SETTINGS', 'config.ProductionConfig')
    REDISTOGO_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
    

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
