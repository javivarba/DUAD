-- SQLite
-- PASO 1: Agregar columna de teléfono (opcional)
ALTER TABLE facturas ADD COLUMN telefono_comprador TEXT;

-- PASO 2: Agregar columna de empleado (obligatoria con DEFAULT)
-- Como es NOT NULL, necesitamos un valor por defecto
ALTER TABLE facturas ADD COLUMN codigo_empleado_cajero TEXT NOT NULL DEFAULT 'EMP000';

-- PASO 3: Verificar la nueva estructura
.schema facturas

-- PASO 4: Actualizar registros existentes con datos reales
UPDATE facturas 
SET telefono_comprador = '+1-555-0101', 
    codigo_empleado_cajero = 'EMP001' 
WHERE numero_factura = 'F001';

UPDATE facturas 
SET telefono_comprador = '+1-555-0102', 
    codigo_empleado_cajero = 'EMP002' 
WHERE numero_factura = 'F002';