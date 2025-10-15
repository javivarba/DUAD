# routes/invoice_routes.py
from flask import Blueprint, request, jsonify, Response
from middleware.auth_decorators import require_auth

# Crear blueprint
invoice_bp = Blueprint('invoices', __name__, url_prefix='/api')

# Las dependencias se inyectarán después
purchase_service = None
jwt_manager = None

def init_invoice_routes(service, jwt_mgr):
    """Inicializa el servicio de compras y JWT manager"""
    global purchase_service, jwt_manager
    purchase_service = service
    jwt_manager = jwt_mgr

@invoice_bp.route('/purchase', methods=['POST'])
@require_auth(lambda: jwt_manager)
def purchase_product(user_info):
    """Endpoint para realizar una compra (usuario y admin)"""
    try:
        data = request.get_json()
        
        if not data:
            return Response(status=400)
        
        # Llamar al service
        result = purchase_service.purchase_product(
            user_id=user_info['id'],
            product_id=data.get('product_id'),
            quantity=data.get('quantity')
        )
        
        if result['success']:
            return jsonify(
                message="Purchase successful",
                invoice_id=result['invoice_id'],
                total_price=result['total_price']
            ), 201
        elif result['error'] == 'Product not found':
            return Response(status=404)
        else:
            return jsonify(error=result['error']), 400
            
    except Exception as e:
        print(f"Purchase route error: {e}")
        return Response(status=500)

@invoice_bp.route('/invoices', methods=['GET'])
@require_auth(lambda: jwt_manager)
def get_invoices(user_info):
    """Endpoint para obtener las facturas del usuario (usuario y admin)"""
    try:
        invoices = purchase_service.get_user_invoices(user_info['id'])
        return jsonify(invoices=invoices), 200
        
    except Exception as e:
        print(f"Get invoices route error: {e}")
        return Response(status=500)