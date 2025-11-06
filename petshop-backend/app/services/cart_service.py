from app import db
from app.models import Cart, CartItem, Product
from app.services.product_service import ProductService
from werkzeug.exceptions import BadRequest, NotFound

class CartService:
    """Servicio para gestionar carritos de compra"""
    
    @staticmethod
    def get_or_create_active_cart(user_id):
        """
        Obtiene el carrito activo del usuario o crea uno nuevo
        """
        cart = Cart.query.filter_by(user_id=user_id, status='active').first()
        
        if not cart:
            cart = Cart(user_id=user_id, status='active')
            db.session.add(cart)
            db.session.commit()
        
        return cart
    
    @staticmethod
    def get_cart_by_id(cart_id):
        """
        Obtiene un carrito por ID
        """
        cart = Cart.query.get(cart_id)
        if not cart:
            raise NotFound(f"Carrito {cart_id} no encontrado")
        return cart
    
    @staticmethod
    def add_item_to_cart(user_id, product_id, quantity):
        """
        Agrega un producto al carrito activo del usuario
        """
        if quantity <= 0:
            raise BadRequest("La cantidad debe ser mayor a 0")
        
        # Verificar que el producto existe y tiene stock
        product = ProductService.get_product_by_id(product_id)
        
        if not product.has_stock(quantity):
            raise BadRequest(f"Stock insuficiente. Disponible: {product.stock}")
        
        # Obtener o crear carrito activo
        cart = CartService.get_or_create_active_cart(user_id)
        
        # Verificar si el producto ya está en el carrito
        cart_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()
        
        if cart_item:
            # Actualizar cantidad
            new_quantity = cart_item.quantity + quantity
            if not product.has_stock(new_quantity):
                raise BadRequest(f"Stock insuficiente. Disponible: {product.stock}")
            cart_item.quantity = new_quantity
        else:
            # Crear nuevo item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=product.price
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return cart
    
    @staticmethod
    def update_cart_item(cart_id, product_id, quantity):
        """
        Actualiza la cantidad de un producto en el carrito
        """
        if quantity <= 0:
            raise BadRequest("La cantidad debe ser mayor a 0")
        
        cart_item = CartItem.query.filter_by(
            cart_id=cart_id,
            product_id=product_id
        ).first()
        
        if not cart_item:
            raise NotFound("Producto no encontrado en el carrito")
        
        # Verificar stock
        product = ProductService.get_product_by_id(product_id)
        if not product.has_stock(quantity):
            raise BadRequest(f"Stock insuficiente. Disponible: {product.stock}")
        
        cart_item.quantity = quantity
        db.session.commit()
        
        return CartService.get_cart_by_id(cart_id)
    
    @staticmethod
    def remove_item_from_cart(cart_id, product_id):
        """
        Elimina un producto del carrito
        """
        cart_item = CartItem.query.filter_by(
            cart_id=cart_id,
            product_id=product_id
        ).first()
        
        if not cart_item:
            raise NotFound("Producto no encontrado en el carrito")
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return CartService.get_cart_by_id(cart_id)
    
    @staticmethod
    def clear_cart(cart_id):
        """
        Elimina todos los items del carrito
        """
        cart = CartService.get_cart_by_id(cart_id)
        
        CartItem.query.filter_by(cart_id=cart_id).delete()
        db.session.commit()
        
        return cart
    
    @staticmethod
    def get_cart_total(cart_id):
        """
        Calcula el total del carrito
        """
        cart = CartService.get_cart_by_id(cart_id)
        return cart.calculate_total()
    
    @staticmethod
    def change_cart_status(cart_id, status):
        """
        Cambia el estado del carrito
        """
        if status not in ['active', 'completed', 'abandoned']:
            raise BadRequest("Estado inválido")
        
        cart = CartService.get_cart_by_id(cart_id)
        cart.status = status
        db.session.commit()
        
        return cart