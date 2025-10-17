from app import db
from app.models import Order, OrderItem, Invoice, Cart, Product
from app.services.cart_service import CartService
from app.services.product_service import ProductService
from app.utils import CacheInvalidator
from werkzeug.exceptions import BadRequest, NotFound
from datetime import datetime

class OrderService:
    """Servicio para gestionar órdenes/ventas"""
    
    @staticmethod
    def create_order_from_cart(user_id, cart_id, address_id, payment_method_id):
        """
        Convierte un carrito en una orden (venta)
        """
        # Obtener el carrito
        cart = CartService.get_cart_by_id(cart_id)
        
        # Validar que el carrito pertenece al usuario
        if cart.user_id != user_id:
            raise BadRequest("El carrito no pertenece al usuario")
        
        # Validar que el carrito tiene items
        if not cart.cart_items:
            raise BadRequest("El carrito está vacío")
        
        # Validar que el carrito está activo
        if cart.status != 'active':
            raise BadRequest("El carrito no está activo")
        
        # Verificar stock de todos los productos
        for cart_item in cart.cart_items:
            product = cart_item.product
            if not product.has_stock(cart_item.quantity):
                raise BadRequest(
                    f"Stock insuficiente para {product.name}. "
                    f"Disponible: {product.stock}, Solicitado: {cart_item.quantity}"
                )
        
        # Calcular total
        total_amount = cart.calculate_total()
        
        # Crear la orden
        order = Order(
            user_id=user_id,
            cart_id=cart_id,
            address_id=address_id,
            payment_method_id=payment_method_id,
            total_amount=total_amount,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Para obtener el order.id
        
        # Crear OrderItems (snapshot) y reducir stock
        for cart_item in cart.cart_items:
            product = cart_item.product
            
            # Crear OrderItem con snapshot del producto
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,  # Snapshot
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,  # Snapshot del precio
                subtotal=cart_item.calculate_subtotal()
            )
            db.session.add(order_item)
            
            # Reducir stock del producto
            product.update_stock(-cart_item.quantity)
        
        # Marcar carrito como completado
        cart.status = 'completed'
        
        # Crear factura
        invoice = OrderService._create_invoice(order)
        
        # Cambiar estado de orden a completado
        order.status = 'completed'

        # Invalidar cache de facturas
        CacheInvalidator.invalidate_invoices()
        
        db.session.commit()
        
        return order
    
    @staticmethod
    def _create_invoice(order):
        """
        Crea una factura para una orden (método interno)
        """
        invoice = Invoice(
            order_id=order.id,
            total_amount=order.total_amount,
            tax_amount=0,  # Por ahora sin impuestos
            status='paid'
        )
        invoice.invoice_number = invoice.generate_invoice_number()
        
        db.session.add(invoice)
        return invoice
    
    @staticmethod
    def get_order_by_id(order_id):
        """
        Obtiene una orden por ID
        """
        order = Order.query.get(order_id)
        if not order:
            raise NotFound(f"Orden {order_id} no encontrada")
        return order
    
    @staticmethod
    def get_orders_by_user(user_id):
        """
        Obtiene todas las órdenes de un usuario
        """
        return Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def get_all_orders():
        """
        Obtiene todas las órdenes (para admin)
        """
        return Order.query.order_by(Order.created_at.desc()).all()
    
    @staticmethod
    def cancel_order(order_id):
        """
        Cancela una orden y restaura el stock
        """
        order = OrderService.get_order_by_id(order_id)
        
        if order.status == 'cancelled':
            raise BadRequest("La orden ya está cancelada")
        
        if order.status == 'returned':
            raise BadRequest("La orden ya fue devuelta")
        
        # Restaurar stock de los productos
        for order_item in order.order_items:
            product = ProductService.get_product_by_id(order_item.product_id)
            product.update_stock(order_item.quantity)
        
        # Cambiar estado
        order.status = 'cancelled'
        
        # Actualizar factura
        if order.invoice:
            order.invoice.status = 'cancelled'
        
        db.session.commit()
        
        return order
    
    @staticmethod
    def return_order(order_id):
        """
        Procesa una devolución y restaura el stock
        """
        order = OrderService.get_order_by_id(order_id)
        
        if order.status != 'completed':
            raise BadRequest("Solo se pueden devolver órdenes completadas")
        
        if order.status == 'returned':
            raise BadRequest("La orden ya fue devuelta")
        
        # Restaurar stock de los productos
        for order_item in order.order_items:
            product = ProductService.get_product_by_id(order_item.product_id)
            product.update_stock(order_item.quantity)
        
        # Cambiar estado
        order.status = 'returned'
        
        # Actualizar factura
        if order.invoice:
            order.invoice.status = 'cancelled'
        
        db.session.commit()
        
        return order