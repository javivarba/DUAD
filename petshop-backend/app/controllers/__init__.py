from app.controllers.auth_controller import auth_bp
from app.controllers.user_controller import user_bp
from app.controllers.product_controller import product_bp
from app.controllers.cart_controller import cart_bp
from app.controllers.order_controller import order_bp
from app.controllers.invoice_controller import invoice_bp
from app.controllers.address_controller import address_bp
from app.controllers.payment_method_controller import payment_method_bp

def register_blueprints(app):
    """
    Registra todos los blueprints en la aplicación Flask
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(invoice_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(payment_method_bp)

__all__ = [
    'auth_bp',
    'user_bp',
    'product_bp',
    'cart_bp',
    'order_bp',
    'invoice_bp',
    'address_bp',
    'payment_method_bp',
    'register_blueprints'
]