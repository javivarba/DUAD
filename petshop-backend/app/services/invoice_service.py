from app import db
from app.models import Invoice
from werkzeug.exceptions import NotFound

class InvoiceService:
    """Servicio para gestionar facturas"""
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        """
        Obtiene una factura por ID
        """
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            raise NotFound(f"Factura {invoice_id} no encontrada")
        return invoice
    
    @staticmethod
    def get_invoice_by_number(invoice_number):
        """
        Obtiene una factura por número de factura
        """
        invoice = Invoice.query.filter_by(invoice_number=invoice_number).first()
        if not invoice:
            raise NotFound(f"Factura {invoice_number} no encontrada")
        return invoice
    
    @staticmethod
    def get_invoice_by_order_id(order_id):
        """
        Obtiene una factura por ID de orden
        """
        invoice = Invoice.query.filter_by(order_id=order_id).first()
        if not invoice:
            raise NotFound(f"Factura para orden {order_id} no encontrada")
        return invoice
    
    @staticmethod
    def get_all_invoices():
        """
        Obtiene todas las facturas
        """
        return Invoice.query.order_by(Invoice.issued_at.desc()).all()
    
    @staticmethod
    def get_invoices_by_status(status):
        """
        Obtiene facturas filtradas por estado
        """
        if status not in ['paid', 'pending', 'cancelled']:
            raise ValueError("Estado inválido")
        
        return Invoice.query.filter_by(status=status).order_by(Invoice.issued_at.desc()).all()