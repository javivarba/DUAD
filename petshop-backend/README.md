# 🐾 Petshop E-commerce Backend

Backend completo para un e-commerce de productos para mascotas desarrollado con Flask, PostgreSQL, Redis y arquitectura en capas.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-Cloud-red.svg)](https://redis.io/)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Ejecutar el Servidor](#️-ejecutar-el-servidor)
- [Testing](#-testing)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [API Endpoints](#-api-endpoints)
- [Cacheo con Redis](#-cacheo-con-redis)
- [Tecnologías](#️-tecnologías)

---

## ✨ Características

### **Módulo de Usuarios y Autenticación** 🔐
- ✅ Registro de usuarios con validación
- ✅ Login con JWT (JSON Web Tokens)
- ✅ Roles: Administrador y Cliente
- ✅ Protección de endpoints por rol
- ✅ Cambio de contraseña

### **Módulo de Productos** 🏷️
- ✅ CRUD completo de productos
- ✅ Gestión automática de stock
- ✅ Categorización de productos
- ✅ Búsqueda y filtrado
- ✅ **Cache con Redis** (5-10 min TTL)

### **Módulo de Ventas** 🛒
- ✅ Carrito de compras (1 activo por usuario)
- ✅ Agregar/eliminar productos del carrito
- ✅ Conversión de carrito a orden
- ✅ Generación automática de facturas
- ✅ Cancelaciones y devoluciones con restauración de stock
- ✅ Direcciones de envío/facturación

### **Sistema de Cacheo** 🚀
- ✅ Redis Cloud como backend
- ✅ Invalidación automática al modificar datos
- ✅ TTL configurado estratégicamente
- ✅ Mejora de performance hasta 90%

### **Testing** 🧪
- ✅ 46 tests automatizados
- ✅ 51% de cobertura de código
- ✅ Tests de servicios y controllers
- ✅ Reporte de cobertura HTML

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10 o superior**
- **PostgreSQL 12 o superior**
- **Git**
- **Cuenta en Redis Cloud** (gratuita - [Crear aquí](https://redis.io/try-free/))

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd petshop-backend
```

### 2. Crear ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

Abre **pgAdmin** o **psql** y ejecuta:
```sql
CREATE DATABASE petshop_ecommerce;
```

---

## ⚙️ Configuración

### 1. Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion

# Database Configuration
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/petshop_ecommerce

# JWT Configuration
JWT_SECRET_KEY=tu-jwt-secret-key-super-segura
JWT_ACCESS_TOKEN_EXPIRES=3600

# Redis Configuration (Redis Cloud)
CACHE_TYPE=redis
CACHE_REDIS_HOST=tu-redis-host.redns.redis-cloud.com
CACHE_REDIS_PORT=12345
CACHE_REDIS_PASSWORD=tu-redis-password
CACHE_REDIS_DB=0
CACHE_DEFAULT_TIMEOUT=300

# Application
DEBUG=True
```

**⚠️ Importante:**
- Reemplaza `TU_PASSWORD` con tu contraseña de PostgreSQL
- Configura las credenciales de Redis Cloud
- En producción, usa claves seguras diferentes

### 2. Ejecutar migraciones
```bash
flask db upgrade
```

Esto creará todas las tablas en la base de datos.

---

## ▶️ Ejecutar el Servidor
```bash
python run.py
```

El servidor estará disponible en: **http://localhost:5000**

### Verificar que funciona

Visita: **http://localhost:5000/health**

Deberías ver:
```json
{
  "status": "ok",
  "message": "Petshop API is running"
}
```

---

## 🧪 Testing

### Ejecutar todos los tests
```bash
python run_tests.py
```

Esto ejecutará:
- ✅ 46 tests automatizados
- 📊 Generará reporte de cobertura en terminal
- 📄 Generará reporte HTML en `htmlcov/index.html`

### Ver reporte de cobertura

Abre en tu navegador: `htmlcov/index.html`

---

## 📁 Estructura del Proyecto
```
petshop-backend/
├── app/
│   ├── __init__.py              # Factory Flask app
│   ├── config.py                # Configuraciones
│   ├── models/                  # 📊 Modelos ORM (Base de Datos)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   ├── order.py
│   │   └── invoice.py
│   ├── services/                # 💼 Lógica de Negocio
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── cart_service.py
│   │   ├── order_service.py
│   │   └── invoice_service.py
│   ├── controllers/             # 🎮 Endpoints REST
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── product_controller.py
│   │   ├── cart_controller.py
│   │   └── order_controller.py
│   ├── middlewares/             # 🛡️ Autenticación
│   │   └── auth_middleware.py
│   └── utils/                   # 🔧 Utilidades
│       └── cache_utils.py
├── tests/                       # 🧪 Tests automatizados
│   ├── test_services/
│   └── test_controllers/
├── migrations/                  # 📁 Migraciones DB
├── .env                         # Variables de entorno
├── .gitignore
├── requirements.txt             # Dependencias
├── README.md                    # Este archivo
├── DOCUMENTACION_TECNICA.md     # Documentación detallada
├── run.py                       # Punto de entrada
└── run_tests.py                 # Script de testing
```

---

## 🌐 API Endpoints

### **Autenticación** 🔐

#### Registro
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "client"  // opcional: "admin" o "client"
}
```

**Respuesta exitosa (201):**
```json
{
  "message": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "client"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Respuesta exitosa (200):**
```json
{
  "message": "Inicio de sesión exitoso",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "client"
  }
}
```

---

### **Usuarios** 👥

Todos los endpoints requieren autenticación JWT.

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| GET | `/api/users/` | Obtener todos los usuarios | Admin |
| GET | `/api/users/<id>` | Obtener usuario por ID | Admin o mismo usuario |
| GET | `/api/users/me` | Obtener usuario actual | Cualquiera |
| PUT | `/api/users/<id>` | Actualizar usuario | Admin o mismo usuario |
| DELETE | `/api/users/<id>` | Eliminar usuario | Admin |
| POST | `/api/users/change-password` | Cambiar contraseña | Cualquiera |

**Ejemplo - Obtener usuario actual:**
```http
GET /api/users/me
Authorization: Bearer <token>
```

---

### **Productos** 🏷️

| Método | Endpoint | Descripción | Rol Requerido | Cache |
|--------|----------|-------------|---------------|-------|
| GET | `/api/products/` | Listar todos los productos | Público | ✅ 5 min |
| GET | `/api/products/?category=alimento` | Filtrar por categoría | Público | ✅ 5 min |
| GET | `/api/products/<id>` | Obtener producto por ID | Público | ✅ 10 min |
| POST | `/api/products/` | Crear producto | Admin | - |
| PUT | `/api/products/<id>` | Actualizar producto | Admin | - |
| DELETE | `/api/products/<id>` | Eliminar producto | Admin | - |
| PATCH | `/api/products/<id>/stock` | Actualizar stock | Admin | - |

**Ejemplo - Listar productos:**
```http
GET /api/products/
```

**Respuesta:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "Alimento para perros",
      "description": "Alimento premium",
      "price": 25000,
      "stock": 100,
      "category": "alimento",
      "image_url": "https://..."
    }
  ]
}
```

**Ejemplo - Crear producto:**
```http
POST /api/products/
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "name": "Juguete para gatos",
  "price": 5000,
  "stock": 50,
  "category": "juguete",
  "description": "Juguete interactivo",
  "image_url": "https://..."
}
```

---

### **Carrito** 🛒

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| GET | `/api/cart/` | Obtener carrito activo | Cliente |
| POST | `/api/cart/items` | Agregar producto | Cliente |
| PUT | `/api/cart/items/<product_id>` | Actualizar cantidad | Cliente |
| DELETE | `/api/cart/items/<product_id>` | Eliminar producto | Cliente |
| DELETE | `/api/cart/clear` | Vaciar carrito | Cliente |

**Ejemplo - Agregar producto al carrito:**
```http
POST /api/cart/items
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_id": 1,
  "quantity": 2
}
```

**Respuesta:**
```json
{
  "message": "Producto agregado al carrito",
  "cart": {
    "id": 1,
    "user_id": 1,
    "status": "active",
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "quantity": 2,
        "unit_price": 25000,
        "subtotal": 50000
      }
    ],
    "total": 50000
  }
}
```

---

### **Órdenes** 📦

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| POST | `/api/orders/` | Crear orden desde carrito | Cliente |
| GET | `/api/orders/` | Listar órdenes | Cliente (propias) / Admin (todas) |
| GET | `/api/orders/<id>` | Obtener orden específica | Cliente (propia) / Admin |
| POST | `/api/orders/<id>/cancel` | Cancelar orden | Admin |
| POST | `/api/orders/<id>/return` | Procesar devolución | Admin |

**Ejemplo - Crear orden:**
```http
POST /api/orders/
Authorization: Bearer <token>
Content-Type: application/json

{
  "address_id": 1,
  "payment_method_id": 1
}
```

**Respuesta:**
```json
{
  "message": "Orden creada exitosamente",
  "order": {
    "id": 1,
    "user_id": 1,
    "total_amount": 50000,
    "status": "completed",
    "items": [...],
    "invoice": {
      "invoice_number": "INV-20251017120000-1",
      "total_amount": 50000,
      "status": "paid"
    }
  }
}
```

---

### **Facturas** 📄

| Método | Endpoint | Descripción | Rol Requerido | Cache |
|--------|----------|-------------|---------------|-------|
| GET | `/api/invoices/` | Listar todas las facturas | Admin | ✅ 10 min |
| GET | `/api/invoices/<id>` | Obtener factura por ID | Cliente (propia) / Admin | ✅ 30 min |
| GET | `/api/invoices/number/<num>` | Obtener por número | Cliente (propia) / Admin | ✅ 30 min |
| GET | `/api/invoices/order/<order_id>` | Obtener por orden | Cliente (propia) / Admin | ✅ 30 min |

---

### **Direcciones** 📍

| Método | Endpoint | Descripción | Rol Requerido |
|--------|----------|-------------|---------------|
| GET | `/api/addresses/` | Listar direcciones del usuario | Cliente |
| GET | `/api/addresses/<id>` | Obtener dirección específica | Cliente (propia) / Admin |
| POST | `/api/addresses/` | Crear dirección | Cliente |
| PUT | `/api/addresses/<id>` | Actualizar dirección | Cliente (propia) / Admin |
| DELETE | `/api/addresses/<id>` | Eliminar dirección | Cliente (propia) / Admin |
| POST | `/api/addresses/<id>/set-default` | Marcar como predeterminada | Cliente |

---

### **Métodos de Pago** 💳

| Método | Endpoint | Descripción | Rol Requerido | Cache |
|--------|----------|-------------|---------------|-------|
| GET | `/api/payment-methods/` | Listar métodos activos | Público | ✅ 1 hora |
| GET | `/api/payment-methods/all` | Listar todos (incluye inactivos) | Admin | - |
| GET | `/api/payment-methods/<id>` | Obtener método específico | Público | ✅ 1 hora |
| POST | `/api/payment-methods/` | Crear método de pago | Admin | - |
| PUT | `/api/payment-methods/<id>` | Actualizar método | Admin | - |
| DELETE | `/api/payment-methods/<id>` | Eliminar método | Admin | - |
| POST | `/api/payment-methods/<id>/activate` | Activar método | Admin | - |
| POST | `/api/payment-methods/<id>/deactivate` | Desactivar método | Admin | - |

---

## 🚀 Cacheo con Redis

### Endpoints Cacheados

| Recurso | TTL | Justificación |
|---------|-----|---------------|
| Productos | 5-10 min | Cambian ocasionalmente |
| Métodos de Pago | 1 hora | Casi nunca cambian |
| Facturas | 30 min | Inmutables una vez creadas |

### Estrategia de Invalidación

El sistema utiliza **invalidación por eliminación**:
```
Usuario Admin actualiza producto
         ↓
CacheInvalidator.invalidate_product(id)
         ↓
Redis elimina cache del producto
         ↓
Próximo request recachea automáticamente
```

### Beneficios Medidos

- ⚡ **Reducción de latencia:** 200ms → 15ms
- 📉 **Carga en DB:** -70%
- 🚀 **Requests concurrentes:** +300%

---

## 🛠️ Tecnologías

### Backend
- **Flask 3.0** - Framework web
- **Flask-SQLAlchemy** - ORM
- **Flask-Migrate** - Migraciones de BD
- **Flask-JWT-Extended** - Autenticación
- **Flask-Caching** - Sistema de cache
- **Flask-CORS** - CORS support

### Base de Datos
- **PostgreSQL 12+** - Base de datos principal
- **Redis Cloud** - Cache y sesiones

### Testing
- **Pytest** - Framework de testing
- **Pytest-Flask** - Integración Flask
- **Pytest-Cov** - Cobertura de código

### Otros
- **python-dotenv** - Variables de entorno
- **Werkzeug** - Hashing de contraseñas

---

## 📚 Documentación Adicional

- 📄 **[Documentación Técnica](DOCUMENTACION_TECNICA.md)** - Justificaciones de decisiones técnicas
- 📊 **Diagrama ER** - Ver sección de base de datos en documentación técnica
- 🧪 **Reporte de Tests** - Ejecutar `python run_tests.py` y ver `htmlcov/index.html`

---

## 👨‍💻 Autor

**Javier Vargas Basulto**  
Proyecto Final - Módulo Backend  
javivarba@gmail.com  
[\[GitHub Profile\]](https://github.com/javivarba)

---

## 📄 Licencia

Este proyecto fue desarrollado como parte de un proyecto académico.

---

## 🤝 Contribuciones

Este es un proyecto académico, sugerencias y feedback son bienvenidos.

---

**Desarrollado con ❤️ usando Flask y Python**