from flask import Blueprint, request, jsonify
from app.services import UserService, CartService
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, Conflict

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registro de nuevos usuarios
    POST /api/auth/register
    Body: {
        "email": "user@example.com",
        "password": "password123",
        "first_name": "Juan",
        "last_name": "Pérez",
        "role": "client"  (opcional, default: client)
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Crear usuario
        user = UserService.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=data.get('role', 'client')
        )
        
        # Crear carrito activo para el usuario
        CartService.get_or_create_active_cart(user.id)
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict()
        }), 201
        
    except Conflict as e:
        return jsonify({'error': str(e)}), 409
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al registrar usuario'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicio de sesión
    POST /api/auth/login
    Body: {
        "email": "user@example.com",
        "password": "password123"
    }
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email y password son requeridos'}), 400
        
        # Autenticar usuario
        user = UserService.authenticate(data['email'], data['password'])
        
        # Crear token JWT
        access_token = create_access_token(
            identity=str(user.id),  # <- Convertir a string
            additional_claims={
                'email': user.email,
                'role': user.role
            }
        )
        
        return jsonify({
            'message': 'Inicio de sesión exitoso',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except BadRequest as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        return jsonify({'error': 'Error al iniciar sesión'}), 500