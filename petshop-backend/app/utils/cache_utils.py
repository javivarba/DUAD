from app import cache

class CacheKeys:
    """
    Constantes para las keys de cache
    Facilita la gestión y evita errores de tipeo
    """
    # Products
    ALL_PRODUCTS = 'all_products'
    PRODUCTS_BY_CATEGORY = 'products_category_{}'
    PRODUCT_DETAIL = 'product_{}'
    
    # Payment Methods
    ALL_PAYMENT_METHODS = 'all_payment_methods'
    ACTIVE_PAYMENT_METHODS = 'active_payment_methods'
    PAYMENT_METHOD_DETAIL = 'payment_method_{}'
    
    # Invoices
    ALL_INVOICES = 'all_invoices'
    INVOICE_BY_ID = 'invoice_{}'
    INVOICE_BY_NUMBER = 'invoice_number_{}'
    INVOICE_BY_ORDER = 'invoice_order_{}'

class CacheInvalidator:
    """
    Maneja la invalidación de cache cuando los datos cambian
    """
    
    @staticmethod
    def invalidate_products():
        """
        Invalida todo el cache relacionado con productos
        Se debe llamar cuando se crea, actualiza o elimina un producto
        """
        cache.delete(CacheKeys.ALL_PRODUCTS)
        # Invalidar cache de todas las categorías
        # (En una implementación real, podrías llevar un registro de categorías)
        cache.delete_many(*[
            CacheKeys.PRODUCTS_BY_CATEGORY.format(cat) 
            for cat in ['alimento', 'juguete', 'accesorio', 'medicina', 'higiene']
        ])
    
    @staticmethod
    def invalidate_product(product_id):
        """
        Invalida el cache de un producto específico
        """
        cache.delete(CacheKeys.PRODUCT_DETAIL.format(product_id))
        CacheInvalidator.invalidate_products()
    
    @staticmethod
    def invalidate_payment_methods():
        """
        Invalida todo el cache relacionado con métodos de pago
        Se debe llamar cuando se crea, actualiza o elimina un método de pago
        """
        cache.delete(CacheKeys.ALL_PAYMENT_METHODS)
        cache.delete(CacheKeys.ACTIVE_PAYMENT_METHODS)
    
    @staticmethod
    def invalidate_payment_method(payment_method_id):
        """
        Invalida el cache de un método de pago específico
        """
        cache.delete(CacheKeys.PAYMENT_METHOD_DETAIL.format(payment_method_id))
        CacheInvalidator.invalidate_payment_methods()
    
    @staticmethod
    def invalidate_invoices():
        """
        Invalida todo el cache relacionado con facturas
        Se debe llamar cuando se crea una nueva factura
        """
        cache.delete(CacheKeys.ALL_INVOICES)
    
    @staticmethod
    def invalidate_invoice(invoice_id, invoice_number=None, order_id=None):
        """
        Invalida el cache de una factura específica
        """
        cache.delete(CacheKeys.INVOICE_BY_ID.format(invoice_id))
        if invoice_number:
            cache.delete(CacheKeys.INVOICE_BY_NUMBER.format(invoice_number))
        if order_id:
            cache.delete(CacheKeys.INVOICE_BY_ORDER.format(order_id))
        CacheInvalidator.invalidate_invoices()