from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def admin_required():
    """
    Decorador para proteger rutas que solo pueden acceder administradores
    Uso: @admin_required()
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            if claims.get('role') != 'admin':
                return jsonify({'error': 'Acceso denegado. Se requiere rol de administrador'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def client_required():
    """
    Decorador para proteger rutas que solo pueden acceder clientes
    Uso: @client_required()
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            if claims.get('role') != 'client':
                return jsonify({'error': 'Acceso denegado. Se requiere rol de cliente'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def role_required(roles):
    """
    Decorador para proteger rutas que requieren roles específicos
    Uso: @role_required(['admin', 'client'])
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            
            if user_role not in roles:
                return jsonify({'error': f'Acceso denegado. Se requiere uno de estos roles: {", ".join(roles)}'}), 403
            
            return fn(*args, **kwargs)
        return decorator
    return wrapper