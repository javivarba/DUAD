from app import db
from app.models import User
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound, Conflict

class UserService:
    """Servicio para gestionar usuarios y autenticación"""
    
    @staticmethod
    def create_user(email, password, first_name, last_name, role='client'):
        """
        Crea un nuevo usuario
        """
        # Validar que el email no exista
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise Conflict(f"El email {email} ya está registrado")
        
        # Validar role
        if role not in ['admin', 'client']:
            raise BadRequest("El rol debe ser 'admin' o 'client'")
        
        # Crear usuario
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise Conflict("Error al crear usuario")
    
    @staticmethod
    def authenticate(email, password):
        """
        Autentica un usuario con email y password
        """
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise BadRequest("Credenciales inválidas")
        
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Obtiene un usuario por ID
        """
        user = User.query.get(user_id)
        if not user:
            raise NotFound(f"Usuario {user_id} no encontrado")
        return user
    
    @staticmethod
    def get_user_by_email(email):
        """
        Obtiene un usuario por email
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound(f"Usuario con email {email} no encontrado")
        return user
    
    @staticmethod
    def get_all_users():
        """
        Obtiene todos los usuarios
        """
        return User.query.all()
    
    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Actualiza un usuario
        Campos permitidos: first_name, last_name, email
        """
        user = UserService.get_user_by_id(user_id)
        
        # Campos permitidos para actualizar
        allowed_fields = ['first_name', 'last_name', 'email']
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                # Validar email único si se está actualizando
                if field == 'email':
                    existing = User.query.filter_by(email=value).first()
                    if existing and existing.id != user_id:
                        raise Conflict(f"El email {value} ya está en uso")
                setattr(user, field, value)
        
        try:
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise Conflict("Error al actualizar usuario")
    
    @staticmethod
    def delete_user(user_id):
        """
        Elimina un usuario
        """
        user = UserService.get_user_by_id(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise BadRequest(f"Error al eliminar usuario: {str(e)}")
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """
        Cambia la contraseña de un usuario
        """
        user = UserService.get_user_by_id(user_id)
        
        if not user.check_password(old_password):
            raise BadRequest("Contraseña actual incorrecta")
        
        user.set_password(new_password)
        db.session.commit()
        return user