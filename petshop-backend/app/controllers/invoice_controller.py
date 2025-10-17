from flask import Blueprint, jsonify
from app.services import InvoiceService
from app import cache
from app.utils import CacheKeys, CacheInvalidator
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import NotFound

invoice_bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')

@invoice_bp.route('/', methods=['GET'])
@jwt_required()
@cache.cached(timeout=600)  # Cache 10 minutos
def get_all_invoices():
    """
    Obtiene todas las facturas (solo admin)
    GET /api/invoices/
    Cache: 10 minutos (TTL=600s)
    Invalida: Al crear una nueva factura
    """
    try:
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Acceso denegado'}), 403
        
        invoices = InvoiceService.get_all_invoices()
        
        return jsonify({
            'invoices': [invoice.to_dict() for invoice in invoices]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener facturas'}), 500

@invoice_bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=1800)  # Cache 30 minutos
def get_invoice(invoice_id):
    """
    Obtiene una factura por ID
    GET /api/invoices/<invoice_id>
    Cache: 30 minutos (TTL=1800s) - las facturas no cambian
    """
    try:
        claims = get_jwt()
        user_id = int(get_jwt_identity())
        
        invoice = InvoiceService.get_invoice_by_id(invoice_id)
        
        # Verificar que es admin o el dueño de la orden
        if claims.get('role') != 'admin' and invoice.order.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Preparar respuesta completa
        invoice_data = invoice.to_dict()
        invoice_data['order'] = invoice.order.to_dict() if invoice.order else None
        
        return jsonify(invoice_data), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener factura'}), 500

@invoice_bp.route('/number/<string:invoice_number>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=1800)  # Cache 30 minutos
def get_invoice_by_number(invoice_number):
    """
    Obtiene una factura por número de factura
    GET /api/invoices/number/<invoice_number>
    Cache: 30 minutos (TTL=1800s)
    """
    try:
        claims = get_jwt()
        user_id = int(get_jwt_identity())
        
        invoice = InvoiceService.get_invoice_by_number(invoice_number)
        
        # Verificar que es admin o el dueño de la orden
        if claims.get('role') != 'admin' and invoice.order.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Preparar respuesta completa
        invoice_data = invoice.to_dict()
        invoice_data['order'] = invoice.order.to_dict() if invoice.order else None
        invoice_data['order_items'] = [item.to_dict() for item in invoice.order.order_items]
        
        return jsonify(invoice_data), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener factura'}), 500

@invoice_bp.route('/order/<int:order_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=1800)  # Cache 30 minutos
def get_invoice_by_order(order_id):
    """
    Obtiene una factura por ID de orden
    GET /api/invoices/order/<order_id>
    Cache: 30 minutos (TTL=1800s)
    """
    try:
        claims = get_jwt()
        user_id = int(get_jwt_identity())
        
        invoice = InvoiceService.get_invoice_by_order_id(order_id)
        
        # Verificar que es admin o el dueño de la orden
        if claims.get('role') != 'admin' and invoice.order.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        # Preparar respuesta completa
        invoice_data = invoice.to_dict()
        invoice_data['order'] = invoice.order.to_dict() if invoice.order else None
        
        return jsonify(invoice_data), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener factura'}), 500