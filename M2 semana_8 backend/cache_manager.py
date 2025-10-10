# cache_manager.py
import redis
from config import RedisConfig

class CacheManager:
    """
    Clase para manejar el caché con Redis
    Gestiona el almacenamiento, recuperación e invalidación de datos
    """
    
    def __init__(self):
        """Inicializa la conexión con Redis usando las credenciales de config.py"""
        try:
            self.redis_client = redis.Redis(
                host=RedisConfig.HOST,
                port=RedisConfig.PORT,
                password=RedisConfig.PASSWORD,
                decode_responses=True  # Para recibir strings en vez de bytes
            )
            
            # Verificar conexión
            connection_status = self.redis_client.ping()
            if connection_status:
                print("✅ Conexión a Redis exitosa")
            else:
                print("❌ No se pudo conectar a Redis")
                
        except redis.ConnectionError as e:
            print(f"❌ Error de conexión a Redis: {e}")
            raise
        except Exception as e:
            print(f"❌ Error inicializando CacheManager: {e}")
            raise
    
    def store_data(self, key, value, time_to_live=None):
        """
        Almacena datos en Redis
        
        Args:
            key: Clave para identificar el dato
            value: Valor a almacenar (string o JSON serializado)
            time_to_live: Tiempo de expiración en segundos (opcional)
        """
        try:
            if time_to_live is None:
                self.redis_client.set(key, value)
                print(f"🔵 Cache creado: '{key}'")
            else:
                self.redis_client.setex(key, time_to_live, value)
                print(f"🔵 Cache creado: '{key}' con TTL de {time_to_live}s")
            return True
            
        except redis.RedisError as error:
            print(f"❌ Error guardando en Redis: {error}")
            return False
    
    def get_data(self, key):
        """
        Obtiene datos del caché
        
        Args:
            key: Clave del dato a recuperar
            
        Returns:
            El valor almacenado o None si no existe
        """
        try:
            value = self.redis_client.get(key)
            
            if value is not None:
                print(f"✅ Cache hit: '{key}'")
                return value
            else:
                print(f"⚠️ Cache miss: '{key}'")
                return None
                
        except redis.RedisError as error:
            print(f"❌ Error obteniendo de Redis: {error}")
            return None
    
    def check_key(self, key):
        """
        Verifica si una clave existe en Redis
        
        Args:
            key: Clave a verificar
            
        Returns:
            tuple: (existe: bool, ttl: int o None)
        """
        try:
            key_exists = self.redis_client.exists(key)
            
            if key_exists:
                ttl = self.redis_client.ttl(key)
                print(f"🔍 Key '{key}' existe (TTL: {ttl}s)")
                return True, ttl
            else:
                print(f"🔍 Key '{key}' no existe")
                return False, None
                
        except redis.RedisError as error:
            print(f"❌ Error verificando key en Redis: {error}")
            return False, None
    
    def delete_data(self, key):
        """
        Elimina una clave específica del caché
        
        Args:
            key: Clave a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        try:
            result = self.redis_client.delete(key)
            
            if result > 0:
                print(f"🗑️ Cache eliminado: '{key}'")
                return True
            else:
                print(f"⚠️ Key '{key}' no existía")
                return False
                
        except redis.RedisError as error:
            print(f"❌ Error eliminando de Redis: {error}")
            return False
    
    def delete_data_with_pattern(self, pattern):
        """
        Elimina todas las claves que coincidan con un patrón
        Útil para invalidar múltiples caches relacionados
        
        Args:
            pattern: Patrón de búsqueda (ej: "frutas:*")
        """
        try:
            deleted_count = 0
            
            # Buscar todas las keys que coincidan con el patrón
            for key in self.redis_client.scan_iter(match=pattern):
                self.redis_client.delete(key)
                deleted_count += 1
            
            if deleted_count > 0:
                print(f"🗑️ {deleted_count} cache(s) eliminado(s) con patrón '{pattern}'")
            else:
                print(f"⚠️ No se encontraron keys con patrón '{pattern}'")
                
        except redis.RedisError as error:
            print(f"❌ Error eliminando con patrón en Redis: {error}")