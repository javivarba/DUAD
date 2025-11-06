# routes/__init__.py
from .auth_routes import auth_bp, init_auth_routes
from .product_routes import product_bp, init_product_routes
from .invoice_routes import invoice_bp, init_invoice_routes

__all__ = [
    'auth_bp', 'init_auth_routes',
    'product_bp', 'init_product_routes',
    'invoice_bp', 'init_invoice_routes'
]