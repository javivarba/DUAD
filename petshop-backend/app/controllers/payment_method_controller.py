from flask import Blueprint, request, jsonify
from app.services import PaymentMethodService
from app import cache
from app.utils import CacheKeys, CacheInvalidator
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.exceptions import NotFound, BadRequest, Conflict

payment_method_bp = Blueprint('payment_methods', __name__, url_prefix='/api/payment-methods')

@payment_method_bp.route('/', methods=['GET'])
@cache.cached(timeout=3600)  # Cache 1 hora
def get_all_payment_methods():
    """
    Obtiene todos los métodos de pago activos (público)
    GET /api/payment-methods/
    Cache: 1 hora (TTL=3600s) - cambian muy raramente
    Invalida: Al crear, actualizar, activar o desactivar métodos de pago
    """
    try:
        payment_methods = PaymentMethodService.get_all_payment_methods(only_active=True)
        
        return jsonify({
            'payment_methods': [pm.to_dict() for pm in payment_methods]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener métodos de pago'}), 500

@payment_method_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_payment_methods_admin():
    """
    Obtiene todos los métodos de pago incluyendo inactivos (solo admin)
    GET /api/payment-methods/all
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        payment_methods = PaymentMethodService.get_all_payment_methods(only_active=False)
        
        return jsonify({
            'payment_methods': [pm.to_dict() for pm in payment_methods]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener métodos de pago'}), 500

@payment_method_bp.route('/<int:payment_method_id>', methods=['GET'])
@cache.cached(timeout=3600)  # Cache 1 hora
def get_payment_method(payment_method_id):
    """
    Obtiene un método de pago específico (público)
    GET /api/payment-methods/<payment_method_id>
    Cache: 1 hora (TTL=3600s)
    Invalida: Al actualizar el método de pago
    """
    try:
        payment_method = PaymentMethodService.get_payment_method_by_id(payment_method_id)
        return jsonify(payment_method.to_dict()), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener método de pago'}), 500

@payment_method_bp.route('/', methods=['POST'])
@jwt_required()
def create_payment_method():
    """
    Crea un nuevo método de pago (solo admin)
    POST /api/payment-methods/
    Body: {
        "name": "SINPE Móvil",
        "description": "Transferencia mediante SINPE",
        "is_active": true
    }
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': 'Campo name es requerido'}), 400
        
        payment_method = PaymentMethodService.create_payment_method(
            name=data['name'],
            description=data.get('description'),
            is_active=data.get('is_active', True)
        )
        
        # Invalidar cache de métodos de pago
        CacheInvalidator.invalidate_payment_methods()
        
        return jsonify({
            'message': 'Método de pago creado exitosamente',
            'payment_method': payment_method.to_dict()
        }), 201
        
    except Conflict as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Error al crear método de pago'}), 500

@payment_method_bp.route('/<int:payment_method_id>', methods=['PUT'])
@jwt_required()
def update_payment_method(payment_method_id):
    """
    Actualiza un método de pago (solo admin)
    PUT /api/payment-methods/<payment_method_id>
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        payment_method = PaymentMethodService.update_payment_method(payment_method_id, **data)
        
        # Invalidar cache del método de pago
        CacheInvalidator.invalidate_payment_method(payment_method_id)
        
        return jsonify({
            'message': 'Método de pago actualizado exitosamente',
            'payment_method': payment_method.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Conflict as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Error al actualizar método de pago'}), 500

@payment_method_bp.route('/<int:payment_method_id>', methods=['DELETE'])
@jwt_required()
def delete_payment_method(payment_method_id):
    """
    Elimina un método de pago (solo admin)
    DELETE /api/payment-methods/<payment_method_id>
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        PaymentMethodService.delete_payment_method(payment_method_id)
        
        # Invalidar cache del método de pago
        CacheInvalidator.invalidate_payment_method(payment_method_id)
        
        return jsonify({'message': 'Método de pago eliminado exitosamente'}), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al eliminar método de pago'}), 500

@payment_method_bp.route('/<int:payment_method_id>/activate', methods=['POST'])
@jwt_required()
def activate_payment_method(payment_method_id):
    """
    Activa un método de pago (solo admin)
    POST /api/payment-methods/<payment_method_id>/activate
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        payment_method = PaymentMethodService.activate_payment_method(payment_method_id)
        
        # Invalidar cache
        CacheInvalidator.invalidate_payment_method(payment_method_id)
        
        return jsonify({
            'message': 'Método de pago activado',
            'payment_method': payment_method.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al activar método de pago'}), 500

@payment_method_bp.route('/<int:payment_method_id>/deactivate', methods=['POST'])
@jwt_required()
def deactivate_payment_method(payment_method_id):
    """
    Desactiva un método de pago (solo admin)
    POST /api/payment-methods/<payment_method_id>/deactivate
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        payment_method = PaymentMethodService.deactivate_payment_method(payment_method_id)
        
        # Invalidar cache
        CacheInvalidator.invalidate_payment_method(payment_method_id)
        
        return jsonify({
            'message': 'Método de pago desactivado',
            'payment_method': payment_method.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al desactivar método de pago'}), 500