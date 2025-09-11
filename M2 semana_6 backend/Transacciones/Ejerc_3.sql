-- =====================================================
-- EJERCICIO 3: TRANSACCIÓN PARA RETORNO DE PRODUCTO
-- 1. Validar que la factura existe en la DB
-- 2. Aumentar el stock del producto en la cantidad que se compró
-- 3. Actualizar la factura y marcarla como retornada
-- =====================================================

-- NOTA: Este script requiere que se hayan ejecutado los Ejercicios 1 y 2
-- para tener facturas disponibles para retornar

-- Primero, agregar el estado 'RETORNADA' a la tabla facturas si no existe
DO $$
BEGIN
    -- Verificar si ya existe el constraint con el estado RETORNADA
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.check_constraints 
        WHERE constraint_name LIKE '%facturas_estado_check%' 
        AND check_clause LIKE '%RETORNADA%'
    ) THEN
        -- Eliminar constraint existente y crear uno nuevo
        ALTER TABLE facturas DROP CONSTRAINT IF EXISTS facturas_estado_check;
        ALTER TABLE facturas ADD CONSTRAINT facturas_estado_check 
        CHECK (estado IN ('PENDIENTE', 'PAGADA', 'CANCELADA', 'RETORNADA'));
        
        RAISE NOTICE '✓ Estado RETORNADA agregado a la tabla facturas';
    END IF;
END $$;

-- =====================================================
-- TRANSACCIÓN PRINCIPAL DE RETORNO
-- =====================================================

DO $$
DECLARE
    -- PARÁMETROS DEL RETORNO (modificar según necesidad)
    v_numero_factura VARCHAR(50) := 'FAC-20250908-094441-1'; -- Número de factura a retornar
    -- O usar ID de factura si prefieres:
    -- v_factura_id INTEGER := 1; -- ID de la factura a retornar
    
    -- VARIABLES INTERNAS
    v_factura_id INTEGER;
    v_usuario_id INTEGER;
    v_estado_actual VARCHAR(20);
    v_fecha_factura TIMESTAMP;
    v_total_factura DECIMAL(10,2);
    v_productos_count INTEGER := 0;
    
    -- Variables para el cursor de productos
    rec RECORD;
BEGIN
    -- INICIAR TRANSACCIÓN DE RETORNO
    BEGIN
        RAISE NOTICE '=== INICIANDO TRANSACCIÓN DE RETORNO ===';
        RAISE NOTICE 'Factura a retornar: %', v_numero_factura;
        
        -- =====================================================
        -- PASO 1: VALIDAR QUE LA FACTURA EXISTE EN LA DB
        -- =====================================================
        
        SELECT f.id, f.usuario_id, f.estado, f.fecha_factura, f.total
        INTO v_factura_id, v_usuario_id, v_estado_actual, v_fecha_factura, v_total_factura
        FROM facturas f 
        WHERE f.numero_factura = v_numero_factura;
        
        -- Verificar si la factura existe
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Error: La factura % no existe en la base de datos', v_numero_factura;
        END IF;
        
        RAISE NOTICE '✓ Factura encontrada: ID %, Usuario: %, Total: $%, Estado: %', 
            v_factura_id, v_usuario_id, v_total_factura, v_estado_actual;
        
        -- Verificar que la factura no esté ya retornada
        IF v_estado_actual = 'RETORNADA' THEN
            RAISE EXCEPTION 'Error: La factura % ya ha sido retornada previamente', v_numero_factura;
        END IF;
        
        -- Verificar que la factura esté en un estado válido para retorno
        IF v_estado_actual NOT IN ('PENDIENTE', 'PAGADA') THEN
            RAISE EXCEPTION 'Error: No se puede retornar una factura con estado %', v_estado_actual;
        END IF;
        
        RAISE NOTICE '✓ Estado de factura válido para retorno: %', v_estado_actual;
        
        -- Contar productos en la factura
        SELECT COUNT(*) INTO v_productos_count
        FROM detalle_facturas 
        WHERE factura_id = v_factura_id;
        
        IF v_productos_count = 0 THEN
            RAISE EXCEPTION 'Error: La factura % no tiene productos asociados', v_numero_factura;
        END IF;
        
        RAISE NOTICE '✓ Factura tiene % producto(s) para retornar', v_productos_count;

        -- =====================================================
        -- PASO 2: AUMENTAR EL STOCK DE CADA PRODUCTO
        -- =====================================================
        
        RAISE NOTICE '--- Procesando retorno de productos ---';
        
        -- Iterar sobre todos los productos de la factura
        FOR rec IN 
            SELECT 
                df.producto_id,
                df.cantidad,
                df.precio_unitario,
                p.nombre as nombre_producto,
                p.stock as stock_actual
            FROM detalle_facturas df
            JOIN productos p ON df.producto_id = p.id
            WHERE df.factura_id = v_factura_id
        LOOP
            -- Verificar que el producto aún existe y está activo
            IF NOT EXISTS (
                SELECT 1 FROM productos 
                WHERE id = rec.producto_id AND activo = TRUE
            ) THEN
                RAISE EXCEPTION 'Error: El producto ID % ya no existe o está inactivo', rec.producto_id;
            END IF;
            
            -- Aumentar el stock del producto
            UPDATE productos 
            SET stock = stock + rec.cantidad
            WHERE id = rec.producto_id;
            
            RAISE NOTICE '✓ Stock actualizado: % | Cantidad retornada: % | Nuevo stock: %', 
                rec.nombre_producto, rec.cantidad, (rec.stock_actual + rec.cantidad);
                
        END LOOP;

        -- =====================================================
        -- PASO 3: ACTUALIZAR LA FACTURA COMO RETORNADA
        -- =====================================================
        
        -- Marcar la factura como retornada
        UPDATE facturas 
        SET estado = 'RETORNADA'
        WHERE id = v_factura_id;
        
        RAISE NOTICE '✓ Factura actualizada: Estado cambiado a RETORNADA';
        
        -- Opcional: Agregar fecha de retorno (requiere modificar estructura)
        -- Si quisieras agregar una columna fecha_retorno:
        -- ALTER TABLE facturas ADD COLUMN IF NOT EXISTS fecha_retorno TIMESTAMP;
        -- UPDATE facturas SET fecha_retorno = CURRENT_TIMESTAMP WHERE id = v_factura_id;

        -- =====================================================
        -- TRANSACCIÓN DE RETORNO COMPLETADA
        -- =====================================================
        RAISE NOTICE '=== RETORNO COMPLETADO EXITOSAMENTE ===';
        RAISE NOTICE 'Factura: % | Total retornado: $% | Productos: %', 
            v_numero_factura, v_total_factura, v_productos_count;

    EXCEPTION
        WHEN OTHERS THEN
            -- En caso de cualquier error, se hace rollback automático
            RAISE NOTICE '❌ ERROR EN EL RETORNO: %', SQLERRM;
            RAISE NOTICE '❌ Todos los cambios han sido revertidos (ROLLBACK)';
            RAISE; -- Re-lanza la excepción
    END;
END $$;

-- =====================================================
-- CONSULTAS PARA VERIFICAR LOS RESULTADOS DEL RETORNO
-- =====================================================

-- Verificar el estado de la factura retornada
SELECT 
    f.numero_factura,
    f.estado,
    f.fecha_factura,
    f.total,
    u.nombre as cliente
FROM facturas f 
JOIN usuarios u ON f.usuario_id = u.id 
WHERE f.numero_factura = 'FAC-20250908-094441-1'; -- Cambiar por tu número de factura

-- Verificar el stock actualizado de los productos
SELECT 
    p.id,
    p.nombre,
    p.stock,
    df.cantidad as cantidad_retornada
FROM productos p
JOIN detalle_facturas df ON p.id = df.producto_id
JOIN facturas f ON df.factura_id = f.id
WHERE f.numero_factura = 'FAC-20250908-094441-1' -- Cambiar por tu número de factura
ORDER BY p.id;

-- Ver todas las facturas y sus estados
SELECT 
    numero_factura,
    estado,
    total,
    fecha_factura
FROM facturas 
ORDER BY fecha_factura DESC;

-- =====================================================
-- TRANSACCIÓN CON VERIFICACIONES ADICIONALES (BONUS)
-- =====================================================

-- Ejemplo de retorno con validaciones más estrictas
DO $$
DECLARE
    v_factura_a_retornar VARCHAR(50) := 'NUMERO_FACTURA_INEXISTENTE'; -- Esto debe fallar
BEGIN
    BEGIN
        RAISE NOTICE '=== PROBANDO RETORNO CON FACTURA INEXISTENTE ===';
        
        -- Intentar retornar factura que no existe
        IF NOT EXISTS (SELECT 1 FROM facturas WHERE numero_factura = v_factura_a_retornar) THEN
            RAISE EXCEPTION 'Factura no encontrada: %', v_factura_a_retornar;
        END IF;
        
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE '❌ Error esperado: %', SQLERRM;
            RAISE NOTICE '✓ El sistema detectó correctamente la factura inexistente';
    END;
END $$;

-- =====================================================
-- SCRIPT PARA HACER MÚLTIPLES RETORNOS (OPCIONAL)
-- =====================================================

-- Si tienes múltiples facturas y quieres retornar todas las pendientes:
/*
DO $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN 
        SELECT numero_factura 
        FROM facturas 
        WHERE estado IN ('PENDIENTE', 'PAGADA')
    LOOP
        RAISE NOTICE 'Procesando retorno de factura: %', rec.numero_factura;
        -- Aquí iría la lógica de retorno para cada factura
    END LOOP;
END $$;
*/