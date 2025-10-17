from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_cors import CORS

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
from app.models import (
    User, Product, Cart, CartItem, 
    Address, PaymentMethod, Order, OrderItem, Invoice
)

def create_app(config_name='development'):
    """
    Factory Pattern para crear la aplicación Flask
    Permite crear múltiples instancias con diferentes configuraciones
    """
    app = Flask(__name__)
    
    # Cargar configuración
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cache.init_app(app)
    CORS(app)
    
    # Registrar blueprints (controllers)
    from app.controllers import register_blueprints
    register_blueprints(app)
    
    # Ruta de prueba
    @app.route('/health')
    def health_check():
        return {'status': 'ok', 'message': 'Petshop API is running'}, 200
    
    return app