# repositories/user_repository.py
from sqlalchemy import insert, select
from models.db import user_table

class UserRepository:
    """
    Repository para operaciones CRUD de usuarios
    Solo acceso a datos, sin lógica de negocio
    """
    
    def __init__(self, engine):
        self.engine = engine
    
    def create_user(self, username, password, role="user"):
        """Inserta un nuevo usuario y retorna su ID"""
        stmt = insert(user_table).returning(user_table.c.id).values(
            username=username, 
            password=password, 
            role=role
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.all()[0]
    
    def get_user_by_credentials(self, username, password):
        """Obtiene un usuario por username y password"""
        stmt = select(user_table).where(
            user_table.c.username == username
        ).where(
            user_table.c.password == password
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            return users[0] if len(users) > 0 else None
    
    def get_user_by_id(self, user_id):
        """Obtiene un usuario por ID"""
        stmt = select(user_table).where(user_table.c.id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            return users[0] if len(users) > 0 else None