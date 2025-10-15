# Fruits API - Sistema de Venta de Frutas

## Descripción
API REST para gestión de inventario y ventas de frutas con autenticación JWT usando RS256 y sistema de caché con Redis.

## Características
- ✅ Autenticación JWT con algoritmo RS256
- ✅ Roles de usuario (admin/user)
- ✅ CRUD de productos (solo admin)
- ✅ Sistema de compras y facturas
- ✅ ORM con SQLAlchemy
- ✅ **Sistema de caché con Redis para optimización de consultas**
- ✅ **Invalidación automática de caché en operaciones de escritura**

## Requisitos Previos
- Python 3.8+
- PostgreSQL
- Redis (instancia local o en la nube)
- OpenSSL (para generar llaves RSA)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd fruits-api

## Arquitectura del Proyecto

El proyecto sigue una **arquitectura en capas** para mantener el código organizado y escalable:

### Estructura de Carpetas

proyecto/
├── models/              # Definiciones de tablas (SQLAlchemy)
│   └── db.py
├── repositories/        # Capa de acceso a datos (CRUD puro)
│   ├── user_repository.py
│   ├── product_repository.py
│   └── invoice_repository.py
├── services/            # Lógica de negocio y caché
│   ├── auth_service.py
│   ├── product_service.py
│   └── purchase_service.py
├── routes/              # Endpoints HTTP (Flask Blueprints)
│   ├── auth_routes.py
│   ├── product_routes.py
│   └── invoice_routes.py
├── middleware/          # Decoradores y middleware
│   └── auth_decorators.py
└── utils/               # Utilidades
├── cache_manager.py
└── JWT_Manager.py

