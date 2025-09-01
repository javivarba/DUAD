-- SQLite
--1. TABLA PRODUCTOS
CREATE TABLE productos (
    codigo TEXT PRIMARY KEY,  -- En SQLite usamos TEXT para los códigos alfanuméricos
    nombre TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    fecha_ingreso DATE NOT NULL,
    marca TEXT NOT NULL
);

-- 2. TABLA FACTURAS
CREATE TABLE facturas (
    numero_factura TEXT PRIMARY KEY,  -- PK como TEXT para códigos como F001, F002
    fecha_compra DATE NOT NULL,
    correo_comprador TEXT NOT NULL CHECK (correo_comprador LIKE '%@%'),
    telefono_comprador TEXT,  -- Nuevo campo para teléfono (opcional)
    codigo_empleado_cajero TEXT NOT NULL,  -- Nuevo campo para empleado cajero
    monto_total DECIMAL(10,2) NOT NULL CHECK (monto_total > 0)
);

-- 3. TABLA RELACIÓN FACTURA-PRODUCTOS (N:M)
-- Esta tabla implementa la relación muchos a muchos
CREATE TABLE factura_productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PK auto-generada
    numero_factura TEXT NOT NULL,
    codigo_producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    monto_parcial DECIMAL(10,2) NOT NULL CHECK (monto_parcial > 0),
    
    -- Claves foráneas
    FOREIGN KEY (numero_factura) REFERENCES facturas(numero_factura) ON DELETE CASCADE,
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo) ON DELETE CASCADE,
    
    -- Índice único compuesto para evitar duplicados
    UNIQUE(numero_factura, codigo_producto)
);

-- 4. TABLA CARRITOS DE COMPRAS (N:M)
-- Relación entre compradores y productos antes de generar factura
CREATE TABLE carritos_compras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- PK auto-generada
    correo_comprador TEXT NOT NULL CHECK (correo_comprador LIKE '%@%'),
    codigo_producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    
    -- Clave foránea
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo) ON DELETE CASCADE,
    
    -- Índice único compuesto
    UNIQUE(correo_comprador, codigo_producto)
);

-- ========================================
-- INSERCIÓN DE DATOS DE EJEMPLO
-- ========================================

-- Insertar productos
INSERT INTO productos (codigo, nombre, precio, fecha_ingreso, marca) VALUES 
('P001', 'Spinnerbait', 4000.00, '2025-07-20', 'Yozuri'),
('P002', 'Jigs', 3500.00, '2025-07-15', 'Mustad'),
('P003', 'Curlsco', 7000.00, '2025-07-20', 'Nakamura'),
('P004', 'Twitchbait', 8500.00, '2025-07-22', 'Yozuri');

-- Insertar facturas
INSERT INTO facturas (numero_factura, fecha_compra, correo_comprador, telefono_comprador, codigo_empleado_cajero, monto_total) VALUES 
('F001', '2025-07-25', 'vito.corleone@godfather.com', '+1-555-0101', 'EMP001', 11000.00),
('F002', '2025-07-26', 'sony.corleone@godfather.com', '+1-555-0102', 'EMP002', 10500.00);

-- Insertar relaciones factura-productos
INSERT INTO factura_productos (numero_factura, codigo_producto, cantidad, monto_parcial) VALUES 
('F001', 'P001', 1, 4000.00),
('F001', 'P003', 1, 7000.00),
('F002', 'P002', 1, 3500.00),
('F002', 'P003', 1, 7000.00);

-- Insertar carritos de compras
INSERT INTO carritos_compras (correo_comprador, codigo_producto, cantidad) VALUES 
('vito.corleone@godfather.com', 'P001', 1),
('vito.corleone@godfather.com', 'P003', 1),
('sony.corleone@godfather.com', 'P002', 1),
('sony.corleone@godfather.com', 'P003', 1);
