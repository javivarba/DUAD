# middleware/auth_decorators.py
from functools import wraps
from flask import request, Response

def require_auth(jwt_manager_getter):
    """
    Decorador simplificado que solo valida el token JWT
    Acepta una función que retorna el jwt_manager
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Obtener jwt_manager (puede ser función o directo)
                jwt_manager = jwt_manager_getter() if callable(jwt_manager_getter) else jwt_manager_getter
                
                token = request.headers.get('Authorization')
                if token is None:
                    return Response(status=401)
                
                token = token.replace("Bearer ", "")
                decoded = jwt_manager.decode(token)
                
                if decoded is None:
                    return Response(status=401)
                
                user_info = {
                    'id': decoded['id'],
                    'role': decoded.get('role', 'user')
                }
                
                return f(user_info, *args, **kwargs)
                
            except Exception as e:
                print(f"Auth error: {e}")
                return Response(status=500)
        
        return decorated_function
    return decorator

def require_role(required_role, jwt_manager_getter):
    """
    Decorador para verificar roles usando solo el JWT
    Acepta una función que retorna el jwt_manager
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Obtener jwt_manager (puede ser función o directo)
                jwt_manager = jwt_manager_getter() if callable(jwt_manager_getter) else jwt_manager_getter
                
                token = request.headers.get('Authorization')
                if token is None:
                    return Response(status=401)
                
                token = token.replace("Bearer ", "")
                decoded = jwt_manager.decode(token)
                
                if decoded is None:
                    return Response(status=401)
                
                user_role = decoded.get('role', 'user')
                
                if user_role != required_role:
                    return Response(status=403)
                
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