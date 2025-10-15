# repositories/invoice_repository.py
from sqlalchemy import insert, select
from models.db import invoices_table

class InvoiceRepository:
    """
    Repository para operaciones CRUD de facturas
    Solo acceso a datos, sin lógica de negocio
    """
    
    def __init__(self, engine):
        self.engine = engine
    
    def create_invoice(self, user_id, product_name, product_price, quantity, total_price):
        """Crea una nueva factura y retorna su ID"""
        stmt = insert(invoices_table).returning(invoices_table.c.id).values(
            user_id=user_id,
            product_name=product_name,
            product_price=product_price,
            quantity=quantity,
            total_price=total_price
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.all()[0]
    
    def get_invoices_by_user(self, user_id):
        """Obtiene todas las facturas de un usuario"""
        stmt = select(invoices_table).where(invoices_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()