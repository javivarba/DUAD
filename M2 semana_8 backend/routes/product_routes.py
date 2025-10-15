# routes/product_routes.py
from flask import Blueprint, request, jsonify, Response
from middleware.auth_decorators import require_role

# Crear blueprint
product_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Las dependencias se inyectarán después
product_service = None
jwt_manager = None

def init_product_routes(service, jwt_mgr):
    """Inicializa el servicio de productos y JWT manager"""
    global product_service, jwt_manager
    product_service = service
    jwt_manager = jwt_mgr

@product_bp.route('/', methods=['GET'])
@require_role('admin', lambda: jwt_manager)
def get_all_products(user_info):
    """Endpoint para obtener todos los productos (solo admin)"""
    try:
        products = product_service.get_all_products()
        return jsonify(products=products), 200
        
    except Exception as e:
        print(f"Get all products route error: {e}")
        return Response(status=500)

@product_bp.route('/<int:product_id>', methods=['GET'])
@require_role('admin', lambda: jwt_manager)
def get_product(user_info, product_id):
    """Endpoint para obtener un producto específico (solo admin)"""
    try:
        product = product_service.get_product_by_id(product_id)
        
        if product is None:
            return Response(status=404)
        
        return jsonify(product), 200
        
    except Exception as e:
        print(f"Get product route error: {e}")
        return Response(status=500)

@product_bp.route('/', methods=['POST'])
@require_role('admin', lambda: jwt_manager)
def create_product(user_info):
    """Endpoint para crear un nuevo producto (solo admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return Response(status=400)
        
        # Llamar al service
        result = product_service.create_product(
            name=data.get('name'),
            price=data.get('price'),
            quantity=data.get('quantity')
        )
        
        if result['success']:
            return jsonify(
                id=result['product_id'], 
                message="Product created successfully"
            ), 201
        else:
            return jsonify(error=result['error']), 400
            
    except Exception as e:
        print(f"Create product route error: {e}")
        return Response(status=500)

@product_bp.route('/<int:product_id>', methods=['PUT'])
@require_role('admin', lambda: jwt_manager)
def update_product(user_info, product_id):
    """Endpoint para actualizar un producto (solo admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return Response(status=400)
        
        # Llamar al service
        result = product_service.update_product(
            product_id=product_id,
            name=data.get('name'),
            price=data.get('price'),
            quantity=data.get('quantity')
        )
        
        if result['success']:
            return jsonify(message="Product updated successfully"), 200
        elif result['error'] == 'Product not found':
            return Response(status=404)
        else:
            return jsonify(error=result['error']), 400
            
    except Exception as e:
        print(f"Update product route error: {e}")
        return Response(status=500)

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@require_role('admin', lambda: jwt_manager)
def delete_product(user_info, product_id):
    """Endpoint para eliminar un producto (solo admin)"""
    try:
        # Llamar al service
        result = product_service.delete_product(product_id)
        
        if result['success']:
            return jsonify(message="Product deleted successfully"), 200
        else:
            return Response(status=404)
            
    except Exception as e:
        print(f"Delete product route error: {e}")
        return Response(status=500)