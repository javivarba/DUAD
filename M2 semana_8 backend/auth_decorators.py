from functools import wraps
from flask import request, Response, jsonify

def require_auth(jwt_manager):
    """
    Decorador simplificado que solo valida el token JWT
    No necesita consultar la BD
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if token is None:
                    return Response(status=401)  # Unauthorized
                
                token = token.replace("Bearer ", "")
                decoded = jwt_manager.decode(token)
                
                if decoded is None:
                    return Response(status=401)  # Invalid token
                
                # En lugar de ir a la BD, creamos un objeto user simple
                # con la información del token
                user_info = {
                    'id': decoded['id'],
                    'role': decoded.get('role', 'user')
                }
                
                # Pasar user info a la función
                return f(user_info, *args, **kwargs)
                
            except Exception as e:
                print(f"Auth error: {e}")
                return Response(status=500)
        
        return decorated_function
    return decorator

def require_role(required_role, jwt_manager):
    """
    Decorador para verificar roles usando solo el JWT
    No consulta la BD
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if token is None:
                    return Response(status=401)
                
                token = token.replace("Bearer ", "")
                decoded = jwt_manager.decode(token)
                
                if decoded is None:
                    return Response(status=401)
                
                # Verificar el rol directamente del token decodificado
                user_role = decoded.get('role', 'user')
                
                if user_role != required_role:
                    return Response(status=403)  # Forbidden
                
                # Crear objeto user_info con datos del token
                user_info = {
                    'id': decoded['id'],
                    'role': user_role
                }
                
                return f(user_info, *args, **kwargs)
                
            except Exception as e:
                print(f"Auth error: {e}")
                return Response(status=500)
        
        return decorated_function
    return decorator