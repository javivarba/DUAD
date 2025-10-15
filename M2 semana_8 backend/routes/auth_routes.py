# routes/auth_routes.py
from flask import Blueprint, request, jsonify, Response

# Crear blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Las dependencias se inyectarán después de crear el blueprint
auth_service = None

def init_auth_routes(service):
    """Inicializa el servicio de autenticación"""
    global auth_service
    auth_service = service

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar un nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data:
            return Response(status=400)
        
        # Llamar al service
        result = auth_service.register_user(
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role', 'user')
        )
        
        if result['success']:
            return jsonify(token=result['token']), 200
        else:
            return jsonify(error=result['error']), 400
            
    except Exception as e:
        print(f"Register route error: {e}")
        return Response(status=500)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión"""
    try:
        data = request.get_json()
        
        if not data:
            return Response(status=400)
        
        # Llamar al service
        result = auth_service.login_user(
            username=data.get('username'),
            password=data.get('password')
        )
        
        if result['success']:
            return jsonify(token=result['token']), 200
        elif result['error'] == 'Invalid credentials':
            return Response(status=403)
        else:
            return jsonify(error=result['error']), 400
            
    except Exception as e:
        print(f"Login route error: {e}")
        return Response(status=500)

@auth_bp.route('/me', methods=['GET'])
def me():
    """Endpoint para obtener información del usuario actual"""
    # Este endpoint necesita el decorador @require_auth
    # Lo agregaremos en el siguiente paso
    from middleware.auth_decorators import require_auth
    from flask import current_app
    
    @require_auth(current_app.jwt_manager)
    def get_me(user_info):
        try:
            return jsonify(
                id=user_info['id'],
                role=user_info['role']
            ), 200
        except Exception as e:
            print(f"Me route error: {e}")
            return Response(status=500)
    
    return get_me()