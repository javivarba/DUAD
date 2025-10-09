from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy import insert, select, update, delete
from datetime import datetime

metadata_obj = MetaData()

# Tabla usuarios con rol
user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("password", String),
    Column("role", String(20), default="user")  # "admin" o "user"
)

# Tabla productos
products_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("price", Float),
    Column("entry_date", DateTime, default=datetime.utcnow),
    Column("quantity", Integer)
)

# Tabla facturas
invoices_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("product_name", String(100)),
    Column("product_price", Float),
    Column("quantity", Integer),
    Column("total_price", Float),
    Column("purchase_date", DateTime, default=datetime.utcnow)
)

class DB_Manager:
    def __init__(self):
        # Cambia estos datos por tu configuración de PostgreSQL
        self.engine = create_engine('postgresql+psycopg2://postgres:12122021@localhost:5432/fruits_db')
        metadata_obj.create_all(self.engine)
    
    # === MÉTODOS USUARIOS ===
    def insert_user(self, username, password, role="user"):
        stmt = insert(user_table).returning(user_table.c.id).values(
            username=username, password=password, role=role
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.all()[0]
    
    def get_user(self, username, password):
        stmt = select(user_table).where(
            user_table.c.username == username
        ).where(user_table.c.password == password)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            return users[0] if len(users) > 0 else None
    
    def get_user_by_id(self, id):
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            return users[0] if len(users) > 0 else None
    
    # === MÉTODOS PRODUCTOS ===
    def insert_product(self, name, price, quantity):
        stmt = insert(products_table).returning(products_table.c.id).values(
            name=name, price=price, quantity=quantity
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.all()[0]
    
    def get_all_products(self):
        stmt = select(products_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()
    
    def get_product_by_id(self, id):
        stmt = select(products_table).where(products_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            products = result.all()
            return products[0] if len(products) > 0 else None
    
    def update_product(self, id, name=None, price=None, quantity=None):
        updates = {}
        if name is not None: updates['name'] = name
        if price is not None: updates['price'] = price
        if quantity is not None: updates['quantity'] = quantity
        
        if updates:
            stmt = update(products_table).where(products_table.c.id == id).values(**updates)
            with self.engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()
                return result.rowcount > 0
        return False
    
    def delete_product(self, id):
        stmt = delete(products_table).where(products_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    def reduce_product_quantity(self, id, quantity):
        stmt = update(products_table).where(products_table.c.id == id).values(
            quantity=products_table.c.quantity - quantity
        )
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount > 0
    
    # === MÉTODOS FACTURAS ===
    def insert_invoice(self, user_id, product_name, product_price, quantity, total_price):
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
        stmt = select(invoices_table).where(invoices_table.c.user_id == user_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return result.all()