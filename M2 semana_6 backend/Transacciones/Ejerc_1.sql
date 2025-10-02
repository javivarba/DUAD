-- =====================================================
-- EJERCICIO 1: PLANTEAR BASE DE DATOS SIMPLE
-- Productos, Usuarios y Facturas con todas las columnas necesarias
-- =====================================================

-- Crear base de datos (opcional, ejecutar solo si es necesario)
-- CREATE DATABASE tienda_online;

-- =====================================================
-- TABLA DE USUARIOS
-- =====================================================
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- TABLA DE PRODUCTOS
-- =====================================================
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- TABLA DE FACTURAS
-- =====================================================
CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    usuario_id INTEGER NOT NULL,
    fecha_factura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
    impuestos DECIMAL(10,2) NOT NULL DEFAULT 0,
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'PENDIENTE' CHECK (estado IN ('PENDIENTE', 'PAGADA', 'CANCELADA')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- =====================================================
-- TABLA DE DETALLE DE FACTURAS
-- =====================================================
CREATE TABLE detalle_facturas (
    id SERIAL PRIMARY KEY,
    factura_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- =====================================================
-- DATOS DE PRUEBA
-- =====================================================

-- Insertar usuarios de prueba
INSERT INTO usuarios (nombre, email, telefono, direccion) VALUES
('Juan Pérez', 'juan.perez@email.com', '555-0101', 'Calle 123, Ciudad'),
('María García', 'maria.garcia@email.com', '555-0102', 'Avenida 456, Ciudad'),
('Carlos López', 'carlos.lopez@email.com', '555-0103', 'Plaza 789, Ciudad');

-- Insertar productos de prueba
INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES
('Comida para Perros Premium', 'Alimento balanceado para perros adultos 15kg', 45.99, 100, 'Alimentación'),
('Collar Antipulgas', 'Collar antipulgas y garrapatas para perros medianos', 12.50, 50, 'Accesorios'),
('Juguete Interactivo Gatos', 'Ratón interactivo con sensor de movimiento', 23.75, 25, 'Juguetes'),
('Arena para Gatos', 'Arena aglomerante sin polvo 10kg', 18.00, 80, 'Higiene'),
('Correa Retráctil', 'Correa extensible hasta 5 metros', 15.25, 30, 'Accesorios');

-- =====================================================
-- CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Verificar usuarios creados
SELECT * FROM usuarios;

-- Verificar productos creados
SELECT * FROM productos;

-- Verificar estructura de tablas
SELECT table_name, column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name IN ('usuarios', 'productos', 'facturas', 'detalle_facturas')
ORDER BY table_name, ordinal_position;