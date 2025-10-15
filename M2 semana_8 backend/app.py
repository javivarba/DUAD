# app.py
from flask import Flask, jsonify

# Importar modelos y configuración
from models.db import DB_Manager

# Importar utils
from utils.cache_manager import CacheManager
from utils.JWT_Manager import JWT_Manager

# Importar repositories
from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from repositories.invoice_repository import InvoiceRepository

# Importar services
from services.auth_service import AuthService
from services.product_service import ProductService
from services.purchase_service import PurchaseService

# Importar blueprints
from routes.auth_routes import auth_bp, init_auth_routes
from routes.product_routes import product_bp, init_product_routes
from routes.invoice_routes import invoice_bp, init_invoice_routes

# Crear aplicación Flask
app = Flask("fruits-api")

# ============================================
# INICIALIZACIÓN DE COMPONENTES
# ============================================

# 1. Inicializar managers de utilidades
db_manager = DB_Manager()
cache_manager = CacheManager()
jwt_manager = JWT_Manager('keys/private_key.pem', 'keys/public_key.pem')

# Hacer jwt_manager accesible globalmente para los decoradores
app.jwt_manager = jwt_manager

# 2. Inicializar repositories (capa de datos)
user_repository = UserRepository(db_manager.engine)
product_repository = ProductRepository(db_manager.engine)
invoice_repository = InvoiceRepository(db_manager.engine)

# 3. Inicializar services (capa de negocio)
auth_service = AuthService(user_repository, jwt_manager)
product_service = ProductService(product_repository, cache_manager)
purchase_service = PurchaseService(product_repository, invoice_repository, cache_manager)

# 4. Inicializar routes (inyectar dependencias)
init_auth_routes(auth_service)
init_product_routes(product_service, jwt_manager)
init_invoice_routes(purchase_service, jwt_manager)

# 5. Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(product_bp)
app.register_blueprint(invoice_bp)

# ============================================
# ENDPOINTS BÁSICOS
# ============================================

@app.route("/liveness")
def liveness():
    """Endpoint para verificar que la API está corriendo"""
    return "<p>Fruits API is running!</p>"

@app.route('/test-jwt')
def test_jwt():
    """Endpoint temporal para probar generación de JWT"""
    test_token = jwt_manager.encode({'id': 1, 'role': 'admin'})
    return jsonify(token_generated=test_token is not None, token=test_token)

# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == '__main__':
    app.run(debug=True)