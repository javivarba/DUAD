from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'cancelled', 'returned', name='order_status'), 
                       nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    invoice = db.relationship('Invoice', backref='order', uselist=False, lazy=True)
    
    def calculate_total(self):
        """Calcula el total de la orden"""
        total = sum(item.subtotal for item in self.order_items)
        return total
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'cart_id': self.cart_id,
            'address_id': self.address_id,
            'payment_method_id': self.payment_method_id,
            'total_amount': float(self.total_amount),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Order {self.id} - User {self.user_id}>'