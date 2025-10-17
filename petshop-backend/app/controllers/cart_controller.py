from flask import Blueprint, request, jsonify
from app.services import CartService
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Obtiene el carrito activo del usuario actual
    GET /api/cart/
    """
    try:
        user_id = int(get_jwt_identity())
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Incluir items del carrito
        cart_data = cart.to_dict()
        cart_data['items'] = [item.to_dict() for item in cart.cart_items]
        cart_data['total'] = float(cart.calculate_total())
        
        return jsonify(cart_data), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener carrito'}), 500

@cart_bp.route('/items', methods=['POST'])
@jwt_required()
def add_item():
    """
    Agrega un producto al carrito
    POST /api/cart/items
    Body: {
        "product_id": 1,
        "quantity": 2
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validar campos requeridos
        if 'product_id' not in data or 'quantity' not in data:
            return jsonify({'error': 'product_id y quantity son requeridos'}), 400
        
        cart = CartService.add_item_to_cart(
            user_id=user_id,
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        
        # Incluir items del carrito
        cart_data = cart.to_dict()
        cart_data['items'] = [item.to_dict() for item in cart.cart_items]
        cart_data['total'] = float(cart.calculate_total())
        
        return jsonify({
            'message': 'Producto agregado al carrito',
            'cart': cart_data
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al agregar producto al carrito'}), 500

@cart_bp.route('/items/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_item(product_id):
    """
    Actualiza la cantidad de un producto en el carrito
    PUT /api/cart/items/<product_id>
    Body: {
        "quantity": 5
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'error': 'Campo quantity es requerido'}), 400
        
        # Obtener carrito activo
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Actualizar item
        cart = CartService.update_cart_item(cart.id, product_id, data['quantity'])
        
        # Incluir items del carrito
        cart_data = cart.to_dict()
        cart_data['items'] = [item.to_dict() for item in cart.cart_items]
        cart_data['total'] = float(cart.calculate_total())
        
        return jsonify({
            'message': 'Cantidad actualizada',
            'cart': cart_data
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al actualizar item'}), 500

@cart_bp.route('/items/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_item(product_id):
    """
    Elimina un producto del carrito
    DELETE /api/cart/items/<product_id>
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Obtener carrito activo
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Eliminar item
        cart = CartService.remove_item_from_cart(cart.id, product_id)
        
        # Incluir items del carrito
        cart_data = cart.to_dict()
        cart_data['items'] = [item.to_dict() for item in cart.cart_items]
        cart_data['total'] = float(cart.calculate_total())
        
        return jsonify({
            'message': 'Producto eliminado del carrito',
            'cart': cart_data
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar producto'}), 500

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """
    Vacía el carrito del usuario
    DELETE /api/cart/clear
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Obtener carrito activo
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Limpiar carrito
        cart = CartService.clear_cart(cart.id)
        
        return jsonify({
            'message': 'Carrito vaciado exitosamente',
            'cart': cart.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al vaciar carrito'}), 500