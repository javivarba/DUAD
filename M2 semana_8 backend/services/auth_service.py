# services/auth_service.py
from repositories.user_repository import UserRepository
from utils.JWT_Manager import JWT_Manager

class AuthService:
    """
    Servicio de autenticación
    Maneja la lógica de negocio de registro y login
    """
    
    def __init__(self, user_repository: UserRepository, jwt_manager: JWT_Manager):
        self.user_repository = user_repository
        self.jwt_manager = jwt_manager
    
    def register_user(self, username, password, role="user"):
        """
        Registra un nuevo usuario y retorna un token JWT
        
        Returns:
            dict: {'success': bool, 'token': str, 'error': str}
        """
        try:
            # Validaciones básicas
            if not username or not password:
                return {'success': False, 'error': 'Username and password are required'}
            
            # Crear usuario
            result = self.user_repository.create_user(username, password, role)
            user_id = result[0]
            
            # Generar token
            token = self.jwt_manager.encode({'id': user_id, 'role': role})
            
            if token:
                return {'success': True, 'token': token}
            else:
                return {'success': False, 'error': 'Failed to generate token'}
                
        except Exception as e:
            print(f"Register service error: {e}")
            return {'success': False, 'error': str(e)}
    
    def login_user(self, username, password):
        """
        Autentica un usuario y retorna un token JWT
        
        Returns:
            dict: {'success': bool, 'token': str, 'error': str}
        """
        try:
            # Validaciones básicas
            if not username or not password:
                return {'success': False, 'error': 'Username and password are required'}
            
            # Buscar usuario
            user = self.user_repository.get_user_by_credentials(username, password)
            
            if user is None:
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Generar token
            user_id = user[0]
            role = user[3]
            token = self.jwt_manager.encode({'id': user_id, 'role': role})
            
            if token:
                return {'success': True, 'token': token}
            else:
                return {'success': False, 'error': 'Failed to generate token'}
                
        except Exception as e:
            print(f"Login service error: {e}")
            return {'success': False, 'error': str(e)}