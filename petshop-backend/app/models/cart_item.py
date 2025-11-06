from app import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    
    def calculate_subtotal(self):
        """Calcula el subtotal del item"""
        return self.quantity * self.unit_price
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.calculate_subtotal())
        }
    
    def __repr__(self):
        return f'<CartItem {self.id} - Cart {self.cart_id}>'