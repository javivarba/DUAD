from app import db
from app.models import Product
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

class ProductService:
    """Servicio para gestionar productos"""
    
    @staticmethod
    def create_product(name, price, stock, description=None, category=None, image_url=None):
        """
        Crea un nuevo producto
        """
        # Validaciones
        if price <= 0:
            raise BadRequest("El precio debe ser mayor a 0")
        
        if stock < 0:
            raise BadRequest("El stock no puede ser negativo")
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category=category,
            image_url=image_url
        )
        
        try:
            db.session.add(product)
            db.session.commit()
            return product
        except IntegrityError:
            db.session.rollback()
            raise BadRequest("Error al crear producto")
    
    @staticmethod
    def get_product_by_id(product_id):
        """
        Obtiene un producto por ID
        """
        product = Product.query.get(product_id)
        if not product:
            raise NotFound(f"Producto {product_id} no encontrado")
        return product
    
    @staticmethod
    def get_all_products(category=None):
        """
        Obtiene todos los productos, opcionalmente filtrados por categoría
        """
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        return query.all()
    
    @staticmethod
    def update_product(product_id, **kwargs):
        """
        Actualiza un producto
        Campos permitidos: name, description, price, stock, category, image_url
        """
        product = ProductService.get_product_by_id(product_id)
        
        # Campos permitidos para actualizar
        allowed_fields = ['name', 'description', 'price', 'stock', 'category', 'image_url']
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                # Validaciones específicas
                if field == 'price' and value <= 0:
                    raise BadRequest("El precio debe ser mayor a 0")
                
                if field == 'stock' and value < 0:
                    raise BadRequest("El stock no puede ser negativo")
                
                setattr(product, field, value)
        
        try:
            db.session.commit()
            return product
        except IntegrityError:
            db.session.rollback()
            raise BadRequest("Error al actualizar producto")
    
    @staticmethod
    def delete_product(product_id):
        """
        Elimina un producto
        """
        product = ProductService.get_product_by_id(product_id)
        
        try:
            db.session.delete(product)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise BadRequest(f"Error al eliminar producto: {str(e)}")
    
    @staticmethod
    def update_stock(product_id, quantity):
        """
        Actualiza el stock de un producto
        quantity puede ser positivo (agregar) o negativo (reducir)
        """
        product = ProductService.get_product_by_id(product_id)
        
        new_stock = product.stock + quantity
        
        if new_stock < 0:
            raise BadRequest(f"Stock insuficiente. Stock actual: {product.stock}")
        
        product.stock = new_stock
        db.session.commit()
        
        return product
    
    @staticmethod
    def check_stock_availability(product_id, quantity):
        """
        Verifica si hay suficiente stock disponible
        """
        product = ProductService.get_product_by_id(product_id)
        return product.has_stock(quantity)