import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'pview')
    DB_USER = os.environ.get('DB_USER', 'pviewuser')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'simsim')
    
    DATABASE_URL = os.environ.get('DATABASE_URL') or \
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Server
    SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.environ.get('SERVER_PORT', '80'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    DB_NAME = os.environ.get('TEST_DB_NAME', 'products_test')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}