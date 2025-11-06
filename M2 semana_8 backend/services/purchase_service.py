# services/purchase_service.py
from repositories.product_repository import ProductRepository
from repositories.invoice_repository import InvoiceRepository
from utils.cache_manager import CacheManager

class PurchaseService:
    """
    Servicio de compras
    Maneja la lógica de negocio de compras y facturas
    """
    
    def __init__(self, product_repository: ProductRepository, 
                 invoice_repository: InvoiceRepository, 
                 cache_manager: CacheManager):
        self.product_repository = product_repository
        self.invoice_repository = invoice_repository
        self.cache_manager = cache_manager
    
    def purchase_product(self, user_id, product_id, quantity):
        """
        Procesa una compra de producto
        
        Returns:
            dict: {'success': bool, 'invoice_id': int, 'total_price': float, 'error': str}
        """
        try:
            # Validaciones básicas
            if quantity <= 0:
                return {'success': False, 'error': 'Quantity must be positive'}
            
            # Obtener producto
            product = self.product_repository.get_product_by_id(product_id)
            
            if product is None:
                return {'success': False, 'error': 'Product not found'}
            
            # Verificar stock
            product_name = product[1]
            product_price = product[2]
            current_stock = product[4]
            
            if current_stock < quantity:
                return {'success': False, 'error': 'Insufficient stock'}
            
            # Calcular total
            total_price = product_price * quantity
            
            # Reducir stock
            self.product_repository.reduce_product_quantity(product_id, quantity)
            
            # Invalidar caché (el stock cambió)
            self.cache_manager.delete_data(f"fruta:{product_id}")
            self.cache_manager.delete_data("frutas:all")
            print(f"🔄 Cache invalidado: fruta:{product_id} y frutas:all (compra realizada)")
            
            # Crear factura
            invoice_result = self.invoice_repository.create_invoice(
                user_id=user_id,
                product_name=product_name,
                product_price=product_price,
                quantity=quantity,
                total_price=total_price
            )
            
            invoice_id = invoice_result[0]
            
            return {
                'success': True,
                'invoice_id': invoice_id,
                'total_price': total_price
            }
            
        except Exception as e:
            print(f"Purchase service error: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_user_invoices(self, user_id):
        """
        Obtiene todas las facturas de un usuario
        
        Returns:
            list: Lista de facturas formateadas
        """
        try:
            invoices = self.invoice_repository.get_invoices_by_user(user_id)
            
            # Formatear facturas
            invoices_list = []
            for inv in invoices:
                invoices_list.append({
                    'id': inv[0],
                    'product_name': inv[2],
                    'product_price': inv[3],
                    'quantity': inv[4],
                    'total_price': inv[5],
                    'purchase_date': inv[6].isoformat() if inv[6] else None
                })
            
            return invoices_list
            
        except Exception as e:
            print(f"Get invoices service error: {e}")
            raise