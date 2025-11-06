# repositories/product_repository.py
from sqlalchemy import insert, select, update, delete
from models.db import products_table

class ProductRepository:
    """
    Repository para operaciones CRUD de productos
    Solo acceso a datos, sin lógica de negocio ni caché
    """
    
    def __init__(self, engine):
        self.engine = engine
    
    def create_product(self, name, price, quantity):
        """Inserta un nuevo producto y retorna su ID"""
        stmt = insert(products_table).returning(products_table.c.id).values(
            name=name, 
            price=price, 
            quantity=quantity
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.all()[0]
    
    def get_all_products(self):
        """Obtiene todos los productos"""
        stmt = select(products_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_product_by_id(self, product_id):
        """Obtiene un producto por ID"""
        stmt = select(products_table).where(products_table.c.id == product_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            products = result.all()
            return products[0] if len(products) > 0 else None
    
    def update_product(self, product_id, name=None, price=None, quantity=None):
        """Actualiza un producto. Retorna True si se actualizó"""
        updates = {}
        if name is not None: 
            updates['name'] = name
        if price is not None: 
            updates['price'] = price
        if quantity is not None: 
            updates['quantity'] = quantity
        
        if updates:
            stmt = update(products_table).where(
                products_table.c.id == product_id
            ).values(**updates)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()
                return result.rowcount > 0
        return False
    
    def delete_product(self, product_id):
        """Elimina un producto. Retorna True si se eliminó"""
        stmt = delete(products_table).where(products_table.c.id == product_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    def reduce_product_quantity(self, product_id, quantity):
        """Reduce la cantidad de un producto"""
        stmt = update(products_table).where(
            products_table.c.id == product_id
        ).values(
            quantity=products_table.c.quantity - quantity
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0