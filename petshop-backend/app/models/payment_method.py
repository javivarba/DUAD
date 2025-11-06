from app import db

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    orders = db.relationship('Order', backref='payment_method', lazy=True)
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<PaymentMethod {self.name}>'