# services/product_service.py
import json
from repositories.product_repository import ProductRepository
from utils.cache_manager import CacheManager

class ProductService:
    """
    Servicio de productos
    Maneja la lógica de negocio de productos + caché
    """
    
    def __init__(self, product_repository: ProductRepository, cache_manager: CacheManager):
        self.product_repository = product_repository
        self.cache_manager = cache_manager
        self.cache_ttl = 3600  # 1 hora
    
    def _format_product(self, product):
        """Formatea un producto de tupla a diccionario"""
        return {
            'id': product[0],
            'name': product[1],
            'price': product[2],
            'entry_date': product[3].isoformat() if product[3] else None,
            'quantity': product[4]
        }
    
    def get_all_products(self):
        """
        Obtiene todos los productos (con caché)
        
        Returns:
            list: Lista de productos formateados
        """
        try:
            cache_key = "frutas:all"
            
            # 1. Intentar obtener del caché
            cached_data = self.cache_manager.get_data(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            # 2. Si no está en caché, consultar repository
            products = self.product_repository.get_all_products()
            
            # 3. Formatear productos
            products_list = [self._format_product(p) for p in products]
            
            # 4. Guardar en caché
            self.cache_manager.store_data(
                cache_key, 
                json.dumps(products_list), 
                time_to_live=self.cache_ttl
            )
            
            return products_list
            
        except Exception as e:
            print(f"Get all products service error: {e}")
            raise
    
    def get_product_by_id(self, product_id):
        """
        Obtiene un producto por ID (con caché)
        
        Returns:
            dict or None: Producto formateado o None si no existe
        """
        try:
            cache_key = f"fruta:{product_id}"
            
            # 1. Intentar obtener del caché
            cached_data = self.cache_manager.get_data(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            # 2. Si no está en caché, consultar repository
            product = self.product_repository.get_product_by_id(product_id)
            
            if product is None:
                return None
            
            # 3. Formatear producto
            product_data = self._format_product(product)
            
            # 4. Guardar en caché
            self.cache_manager.store_data(
                cache_key, 
                json.dumps(product_data), 
                time_to_live=self.cache_ttl
            )
            
            return product_data
            
        except Exception as e:
            print(f"Get product by id service error: {e}")
            raise
    
    def create_product(self, name, price, quantity):
        """
        Crea un nuevo producto e invalida caché
        
        Returns:
            dict: {'success': bool, 'product_id': int, 'error': str}
        """
        try:
            # Validaciones
            if not name or price <= 0 or quantity < 0:
                return {'success': False, 'error': 'Invalid product data'}
            
            # Crear producto
            result = self.product_repository.create_product(name, price, quantity)
            product_id = result[0]
            
            # Invalidar caché de lista completa
            self.cache_manager.delete_data("frutas:all")
            print("🔄 Cache invalidado: frutas:all (nueva fruta creada)")
            
            return {'success': True, 'product_id': product_id}
            
        except Exception as e:
            print(f"Create product service error: {e}")
            return {'success': False, 'error': str(e)}
    
    def update_product(self, product_id, name=None, price=None, quantity=None):
        """
        Actualiza un producto e invalida caché
        
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            # Verificar que el producto existe
            product = self.product_repository.get_product_by_id(product_id)
            if product is None:
                return {'success': False, 'error': 'Product not found'}
            
            # Actualizar producto
            success = self.product_repository.update_product(
                product_id, 
                name=name, 
                price=price, 
                quantity=quantity
            )
            
            if success:
                # Invalidar caché específico y lista completa
                self.cache_manager.delete_data(f"fruta:{product_id}")
                self.cache_manager.delete_data("frutas:all")
                print(f"🔄 Cache invalidado: fruta:{product_id} y frutas:all")
                return {'success': True}
            else:
                return {'success': False, 'error': 'Update failed'}
                
        except Exception as e:
            print(f"Update product service error: {e}")
            return {'success': False, 'error': str(e)}
    
    def delete_product(self, product_id):
        """
        Elimina un producto e invalida caché
        
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            # Eliminar producto
            success = self.product_repository.delete_product(product_id)
            
            if success:
                # Invalidar caché específico y lista completa
                self.cache_manager.delete_data(f"fruta:{product_id}")
                self.cache_manager.delete_data("frutas:all")
                print(f"🔄 Cache invalidado: fruta:{product_id} y frutas:all")
                return {'success': True}
            else:
                return {'success': False, 'error': 'Product not found'}
                
        except Exception as e:
            print(f"Delete product service error: {e}")
            return {'success': False, 'error': str(e)}