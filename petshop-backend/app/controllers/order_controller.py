from flask import Blueprint, request, jsonify
from app.services import OrderService, CartService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import NotFound, BadRequest

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """
    Crea una orden desde el carrito activo
    POST /api/orders/
    Body: {
        "address_id": 1,
        "payment_method_id": 1
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validar campos requeridos
        if 'address_id' not in data or 'payment_method_id' not in data:
            return jsonify({'error': 'address_id y payment_method_id son requeridos'}), 400
        
        # Obtener carrito activo
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Crear orden
        order = OrderService.create_order_from_cart(
            user_id=user_id,
            cart_id=cart.id,
            address_id=data['address_id'],
            payment_method_id=data['payment_method_id']
        )
        
        # Preparar respuesta con items
        order_data = order.to_dict()
        order_data['items'] = [item.to_dict() for item in order.order_items]
        order_data['invoice'] = order.invoice.to_dict() if order.invoice else None
        
        return jsonify({
            'message': 'Orden creada exitosamente',
            'order': order_data
        }), 201
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error al crear orden: {str(e)}'}), 500

@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    """
    Obtiene las órdenes del usuario actual o todas (si es admin)
    GET /api/orders/
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        if claims.get('role') == 'admin':
            # Admin ve todas las órdenes
            orders = OrderService.get_all_orders()
        else:
            # Usuario ve solo sus órdenes
            orders = OrderService.get_orders_by_user(user_id)
        
        return jsonify({
            'orders': [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener órdenes'}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    Obtiene una orden específica
    GET /api/orders/<order_id>
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        order = OrderService.get_order_by_id(order_id)
        
        # Verificar que es admin o el dueño de la orden
        if claims.get('role') != 'admin' and order.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Preparar respuesta completa
        order_data = order.to_dict()
        order_data['items'] = [item.to_dict() for item in order.order_items]
        order_data['invoice'] = order.invoice.to_dict() if order.invoice else None
        order_data['address'] = order.address.to_dict() if order.address else None
        order_data['payment_method'] = order.payment_method.to_dict() if order.payment_method else None
        
        return jsonify(order_data), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener orden'}), 500

@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """
    Cancela una orden (solo admin)
    POST /api/orders/<order_id>/cancel
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        order = OrderService.cancel_order(order_id)
        
        return jsonify({
            'message': 'Orden cancelada exitosamente',
            'order': order.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al cancelar orden'}), 500

@order_bp.route('/<int:order_id>/return', methods=['POST'])
@jwt_required()
def return_order(order_id):
    """
    Procesa una devolución (solo admin)
    POST /api/orders/<order_id>/return
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        order = OrderService.return_order(order_id)
        
        return jsonify({
            'message': 'Devolución procesada exitosamente',
            'order': order.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al procesar devolución'}), 500