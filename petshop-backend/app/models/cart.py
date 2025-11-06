from app import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum('active', 'completed', 'abandoned', name='cart_status'), 
                       nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    cart_items = db.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    
    def calculate_total(self):
        """Calcula el total del carrito"""
        total = sum(item.quantity * item.unit_price for item in self.cart_items)
        return total
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Cart {self.id} - User {self.user_id}>'