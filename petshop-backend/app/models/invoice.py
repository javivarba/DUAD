from app import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    # Columnas
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    invoice_number = db.Column(db.String(50), nullable=False, unique=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.Enum('paid', 'pending', 'cancelled', name='invoice_status'), 
                       nullable=False, default='pending')
    issued_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relaciones ya definidas a través de backref en Order
    
    def generate_invoice_number(self):
        """Genera un número de factura único"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'INV-{timestamp}-{self.order_id}'
    
    def to_dict(self):
        """Convierte el objeto a diccionario"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'invoice_number': self.invoice_number,
            'total_amount': float(self.total_amount),
            'tax_amount': float(self.tax_amount),
            'status': self.status,
            'issued_at': self.issued_at.isoformat() if self.issued_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'