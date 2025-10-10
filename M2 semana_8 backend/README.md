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