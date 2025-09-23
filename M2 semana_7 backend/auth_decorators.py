from functools import wraps
from flask import request, Response, jsonify

def require_auth(db_manager, jwt_manager):
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
                
                user_id = decoded['id']
                user = db_manager.get_user_by_id(user_id)
                
                if user is None:
                    return Response(status=401)
                
                # Pasar user info a la función
                return f(user, *args, **kwargs)
                
            except Exception as e:
                print(f"Auth error: {e}")
                return Response(status=500)
        
        return decorated_function
    return decorator

def require_role(required_role, db_manager, jwt_manager):
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
                
                user_id = decoded['id']
                user = db_manager.get_user_by_id(user_id)
                
                if user is None:
                    return Response(status=401)
                
                if user[3] != required_role:  # user[3] es el role
                    return Response(status=403)  # Forbidden
                
                return f(user, *args, **kwargs)
                
            except Exception as e:
                print(f"Auth error: {e}")
                return Response(status=500)
        
        return decorated_function
    return decorator