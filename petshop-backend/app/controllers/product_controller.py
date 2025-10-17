from flask import Blueprint, request, jsonify
from app.services import ProductService
from app import cache
from app.utils import CacheKeys, CacheInvalidator
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.exceptions import NotFound, BadRequest

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.route('/', methods=['GET'])
@cache.cached(timeout=300, query_string=True)  # Cache 5 minutos, considera query params
def get_all_products():
    """
    Obtiene todos los productos (público)
    GET /api/products/?category=alimento
    Cache: 5 minutos (TTL=300s)
    Invalida: Al crear, actualizar o eliminar productos
    """
    try:
        category = request.args.get('category')
        products = ProductService.get_all_products(category=category)
        
        return jsonify({
            'products': [product.to_dict() for product in products]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener productos'}), 500

@product_bp.route('/<int:product_id>', methods=['GET'])
@cache.cached(timeout=600)  # Cache 10 minutos
def get_product(product_id):
    """
    Obtiene un producto por ID (público)
    GET /api/products/<product_id>
    Cache: 10 minutos (TTL=600s)
    Invalida: Al actualizar o eliminar el producto
    """
    try:
        product = ProductService.get_product_by_id(product_id)
        return jsonify(product.to_dict()), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener producto'}), 500

@product_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """
    Crea un nuevo producto (solo admin)
    POST /api/products/
    Body: {
        "name": "Alimento para perros",
        "description": "Alimento premium",
        "price": 25000,
        "stock": 100,
        "category": "alimento",
        "image_url": "https://..."
    }
    """
    try:
        # Verificar que es admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['name', 'price', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        product = ProductService.create_product(
            name=data['name'],
            price=data['price'],
            stock=data['stock'],
            description=data.get('description'),
            category=data.get('category'),
            image_url=data.get('image_url')
        )
        
        # Invalidar cache de productos
        CacheInvalidator.invalidate_products()  # <- AGREGAR ESTA LÍNEA
        
        return jsonify({
            'message': 'Producto creado exitosamente',
            'product': product.to_dict()
        }), 201
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear producto'}), 500

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """
    Actualiza un producto (solo admin)
    PUT /api/products/<product_id>
    Body: {
        "name": "Nuevo nombre",
        "price": 30000,
        "stock": 50
    }
    """
    try:
        # Verificar que es admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        product = ProductService.update_product(product_id, **data)
        
        # Invalidar cache del producto
        CacheInvalidator.invalidate_product(product_id)  # <- AGREGAR ESTA LÍNEA
        
        return jsonify({
            'message': 'Producto actualizado exitosamente',
            'product': product.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al actualizar producto'}), 500

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    Elimina un producto (solo admin)
    DELETE /api/products/<product_id>
    """
    try:
        # Verificar que es admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        ProductService.delete_product(product_id)
        
        # Invalidar cache del producto
        CacheInvalidator.invalidate_product(product_id)  # <- AGREGAR ESTA LÍNEA
        
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al eliminar producto'}), 500

@product_bp.route('/<int:product_id>/stock', methods=['PATCH'])
@jwt_required()
def update_stock(product_id):
    """
    Actualiza el stock de un producto (solo admin)
    PATCH /api/products/<product_id>/stock
    Body: {
        "quantity": 50  (positivo para agregar, negativo para reducir)
    }
    """
    try:
        # Verificar que es admin
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'error': 'Campo quantity es requerido'}), 400
        
        product = ProductService.update_stock(product_id, data['quantity'])
        
        # Invalidar cache del producto
        CacheInvalidator.invalidate_product(product_id)  # <- AGREGAR ESTA LÍNEA
        
        return jsonify({
            'message': 'Stock actualizado exitosamente',
            'product': product.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al actualizar stock'}), 500