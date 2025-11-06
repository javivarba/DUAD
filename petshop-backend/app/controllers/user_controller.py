from flask import Blueprint, request, jsonify
from app.services import UserService
from app.middlewares import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import NotFound, BadRequest, Conflict

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required()
def get_all_users():
    """
    Obtiene todos los usuarios (solo admin)
    GET /api/users/
    """
    try:
        users = UserService.get_all_users()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuarios'}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Obtiene un usuario por ID
    GET /api/users/<user_id>
    """
    try:
        # Verificar que es admin o el mismo usuario
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        if claims.get('role') != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        user = UserService.get_user_by_id(user_id)
        return jsonify(user.to_dict()), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuario'}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Actualiza un usuario
    PUT /api/users/<user_id>
    Body: {
        "first_name": "Juan",
        "last_name": "Pérez",
        "email": "nuevo@example.com"
    }
    """
    try:
        # Verificar que es admin o el mismo usuario
        current_user_id = int(get_jwt_identity())
        claims = get_jwt()
        
        if claims.get('role') != 'admin' and current_user_id != user_id:
            return jsonify({'error': 'Acceso denegado'}), 403
        
        data = request.get_json()
        user = UserService.update_user(user_id, **data)
        
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Conflict as e:
        return jsonify({'error': str(e)}), 409
    except Exception as e:
        return jsonify({'error': 'Error al actualizar usuario'}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required()
def delete_user(user_id):
    """
    Elimina un usuario (solo admin)
    DELETE /api/users/<user_id>
    """
    try:
        UserService.delete_user(user_id)
        
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al eliminar usuario'}), 500

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Obtiene el usuario actual (basado en el token)
    GET /api/users/me
    """
    try:
        current_user_id = int(get_jwt_identity())
        user = UserService.get_user_by_id(current_user_id)
        return jsonify(user.to_dict()), 200
        
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener usuario actual'}), 500

@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Cambia la contraseña del usuario actual
    POST /api/users/change-password
    Body: {
        "old_password": "password123",
        "new_password": "newpassword456"
    }
    """
    try:
        current_user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if 'old_password' not in data or 'new_password' not in data:
            return jsonify({'error': 'old_password y new_password son requeridos'}), 400
        
        UserService.change_password(
            current_user_id,
            data['old_password'],
            data['new_password']
        )
        
        return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al cambiar contraseña'}), 500