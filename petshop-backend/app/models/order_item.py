from app import db

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)  # Snapshot del nombre
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Snapshot del precio
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relaciones ya definidas a través de backref en Order y Product
    
    def calculate_subtotal(self):
        """Calcula el subtotal del item"""
        return self.quantity * self.unit_price
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal)
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id} - Order {self.order_id}>'