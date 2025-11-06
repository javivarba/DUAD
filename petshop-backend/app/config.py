import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Cache Configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Redis Configuration (si CACHE_TYPE es redis)
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.getenv('CACHE_REDIS_PORT', 6379))
    CACHE_REDIS_PASSWORD = os.getenv('CACHE_REDIS_PASSWORD', None)
    CACHE_REDIS_DB = int(os.getenv('CACHE_REDIS_DB', 0))
    
    # URL completa de Redis
    if CACHE_TYPE == 'redis' and CACHE_REDIS_PASSWORD:
        CACHE_REDIS_URL = f"redis://:{CACHE_REDIS_PASSWORD}@{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"
    elif CACHE_TYPE == 'redis':
        CACHE_REDIS_URL = f"redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"
    
class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/petshop_ecommerce'
    )
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    CACHE_TYPE = 'null'  # <- AGREGAR ESTA LÍNEA (deshabilita cache en tests)

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}