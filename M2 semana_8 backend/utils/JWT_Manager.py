import jwt
from datetime import datetime, timedelta

class JWT_Manager:
    def __init__(self, private_key_path, public_key_path):
        try:
            # Leer llave privada (sin contraseña)
            with open(private_key_path, 'r') as f:
                self.private_key = f.read()
            
            # Leer llave pública
            with open(public_key_path, 'r') as f:
                self.public_key = f.read()
            
            self.algorithm = 'RS256'
            print("✅ JWT Manager inicializado correctamente con RS256")
            
        except FileNotFoundError as e:
            print(f"❌ Error: No se encontraron las llaves RSA: {e}")
            print("📋 Ejecuta estos comandos para generar las llaves:")
            print("   mkdir keys")
            print("   openssl genpkey -algorithm RSA -out keys/private_key.pem -pkcs8")
            print("   openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem")
            raise
        except Exception as e:
            print(f"❌ Error inicializando JWT Manager: {e}")
            raise
    
    def encode(self, data):
        try:
            # Agregar expiración (24 horas) y timestamp de creación
            data['exp'] = datetime.utcnow() + timedelta(hours=24)
            data['iat'] = datetime.utcnow()
            
            encoded = jwt.encode(data, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            print(f"Error encoding JWT: {e}")
            return None
    
    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None
        except Exception as e:
            print(f"Error decoding JWT: {e}")
            return None