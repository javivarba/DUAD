from flask import Blueprint, request, jsonify
from app.services import AddressService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import NotFound, BadRequest

address_bp = Blueprint('addresses', __name__, url_prefix='/api/addresses')

@address_bp.route('/', methods=['GET'])
@jwt_required()
def get_addresses():
    """
    Obtiene todas las direcciones del usuario actual
    GET /api/addresses/
    """
    try:
        user_id = get_jwt_identity()
        addresses = AddressService.get_addresses_by_user(user_id)
        
        return jsonify({
            'addresses': [address.to_dict() for address in addresses]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener direcciones'}), 500

@address_bp.route('/<int:address_id>', methods=['GET'])
@jwt_required()
def get_address(address_id):
    """
    Obtiene una dirección específica
    GET /api/addresses/<address_id>
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        address = AddressService.get_address_by_id(address_id)
        
        # Verificar que es admin o el dueño de la dirección
        if claims.get('role') != 'admin' and address.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        return jsonify(address.to_dict()), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener dirección'}), 500

@address_bp.route('/', methods=['POST'])
@jwt_required()
def create_address():
    """
    Crea una nueva dirección
    POST /api/addresses/
    Body: {
        "full_name": "Juan Pérez",
        "phone": "88888888",
        "address_line1": "Calle 123",
        "address_line2": "Apto 4B",
        "city": "San José",
        "state": "San José",
        "postal_code": "10101",
        "country": "Costa Rica",
        "is_default": false
    }
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['full_name', 'phone', 'address_line1', 'city', 'state', 'postal_code']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        address = AddressService.create_address(
            user_id=user_id,
            full_name=data['full_name'],
            phone=data['phone'],
            address_line1=data['address_line1'],
            address_line2=data.get('address_line2'),
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data.get('country', 'Costa Rica'),
            is_default=data.get('is_default', False)
        )
        
        return jsonify({
            'message': 'Dirección creada exitosamente',
            'address': address.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Error al crear dirección'}), 500

@address_bp.route('/<int:address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    """
    Actualiza una dirección
    PUT /api/addresses/<address_id>
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        address = AddressService.get_address_by_id(address_id)
        
        # Verificar que es admin o el dueño de la dirección
        if claims.get('role') != 'admin' and address.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        address = AddressService.update_address(address_id, **data)
        
        return jsonify({
            'message': 'Dirección actualizada exitosamente',
            'address': address.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al actualizar dirección'}), 500

@address_bp.route('/<int:address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    """
    Elimina una dirección
    DELETE /api/addresses/<address_id>
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        address = AddressService.get_address_by_id(address_id)
        
        # Verificar que es admin o el dueño de la dirección
        if claims.get('role') != 'admin' and address.user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        AddressService.delete_address(address_id)
        
        return jsonify({'message': 'Dirección eliminada exitosamente'}), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al eliminar dirección'}), 500

@address_bp.route('/<int:address_id>/set-default', methods=['POST'])
@jwt_required()
def set_default(address_id):
    """
    Establece una dirección como predeterminada
    POST /api/addresses/<address_id>/set-default
    """
    try:
        user_id = int(get_jwt_identity())
        address = AddressService.set_default_address(address_id, user_id)
        
        return jsonify({
            'message': 'Dirección establecida como predeterminada',
            'address': address.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al establecer dirección predeterminada'}), 500