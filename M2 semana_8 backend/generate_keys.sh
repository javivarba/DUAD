

# Script para generar llaves RSA
# Este script SÍ se puede subir al repo

echo "🔑 Generando llaves RSA para JWT..."

# Crear directorio si no existe
mkdir -p keys

# Generar llave privada
openssl genpkey -algorithm RSA -out keys/private_key.pem -pkeyopt rsa_keygen_bits:2048

# Generar llave pública desde la privada
openssl rsa -pubout -in keys/private_key.pem -out keys/public_key.pem

echo "✅ Llaves generadas exitosamente en el directorio 'keys/'"
echo "⚠️  Recuerda: NUNCA subas estas llaves al repositorio"