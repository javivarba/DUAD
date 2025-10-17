# 🚀 Guía de Instalación - Petshop Backend

## 📋 Requisitos Previos
- Python 3.10+
- PostgreSQL 12+
- Cuenta en Redis Cloud (gratuita)

## ⚙️ Configuración Paso a Paso

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd petshop-backend
```

### 2. Crear ambiente virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL
```bash
# Crear la base de datos
createdb petshop_ecommerce

# O desde psql/pgAdmin:
CREATE DATABASE petshop_ecommerce;
```

### 5. Configurar Redis Cloud
1. Ir a https://redis.io/try-free/
2. Crear cuenta gratuita
3. Crear nueva base de datos
4. Copiar: Host, Port, Password

### 6. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales:
# - DATABASE_URL con tu password de PostgreSQL
# - SECRET_KEY (generar uno aleatorio)
# - JWT_SECRET_KEY (generar uno aleatorio)
# - Redis credentials (host, port, password)
```

**Generar claves secretas:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 7. Ejecutar migraciones
```bash
flask db upgrade
```

### 8. Poblar base de datos (opcional)
```bash
python seed_data.py
```

Esto creará:
- 1 admin: `admin@petshop.com` / `admin123`
- 3 clientes: `juan.perez@email.com` / `client123` (y otros)
- 15 productos
- 4 métodos de pago
- 3 órdenes de ejemplo

### 9. Ejecutar servidor
```bash
python run.py
```

Servidor disponible en: http://localhost:5000

### 10. Verificar funcionamiento
```bash
# Health check
curl http://localhost:5000/health

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@petshop.com","password":"admin123"}'
```

### 11. Ejecutar tests
```bash
python run_tests.py
```

## 📚 Documentación
- **README.md** - Documentación completa de la API
- **DOCUMENTACION_TECNICA.md** - Justificaciones técnicas

## 🆘 Troubleshooting

**Error de conexión a PostgreSQL:**
- Verificar que PostgreSQL esté corriendo
- Verificar credenciales en .env

**Error de conexión a Redis:**
- Verificar credenciales de Redis Cloud
- Verificar que CACHE_TYPE='redis' en .env

**Tests fallan:**
- Verificar que todas las dependencias estén instaladas
- Ejecutar `flask db upgrade` primero