-- =====================================================
-- EJERCICIO 2: TRANSACCIÓN PARA REALIZAR UNA COMPRA
-- 1. Validar que existe stock del producto
-- 2. Validar que el usuario existe  
-- 3. Crear la factura con el usuario relacionado
-- 4. Reducir el stock del producto
-- =====================================================

-- NOTA: Este script requiere que primero se ejecute el Ejercicio 1
-- para crear las tablas y datos de prueba necesarios

-- =====================================================
-- TRANSACCIÓN PRINCIPAL DE COMPRA
-- =====================================================

DO $$
DECLARE
    -- PARÁMETROS DE LA COMPRA (modificar según necesidad)
    v_usuario_id INTEGER := 1;  -- ID del usuario que compra
    v_producto_id INTEGER := 1; -- ID del producto a comprar
    v_cantidad INTEGER := 2;    -- Cantidad a comprar
    
    -- VARIABLES INTERNAS
    v_numero_factura VARCHAR(50);
    v_precio_unitario DECIMAL(10,2);
    v_subtotal DECIMAL(10,2);
    v_impuestos DECIMAL(10,2);
    v_total DECIMAL(10,2);
    v_factura_id INTEGER;
    v_stock_actual INTEGER;
    v_usuario_existe BOOLEAN := FALSE;
BEGIN
    -- INICIAR TRANSACCIÓN
    BEGIN
        RAISE NOTICE '=== INICIANDO TRANSACCIÓN DE COMPRA ===';
        
        -- =====================================================
        -- PASO 1: VALIDAR QUE EL USUARIO EXISTE
        -- =====================================================
        SELECT EXISTS(
            SELECT 1 FROM usuarios 
            WHERE id = v_usuario_id AND activo = TRUE
        ) INTO v_usuario_existe;
        
        IF NOT v_usuario_existe THEN
            RAISE EXCEPTION 'Error: El usuario con ID % no existe o está inactivo', v_usuario_id;
        END IF;
        
        RAISE NOTICE '✓ Usuario validado correctamente: ID %', v_usuario_id;

        -- =====================================================
        -- PASO 2: VALIDAR QUE EXISTE STOCK DEL PRODUCTO
        -- =====================================================
        SELECT stock, precio INTO v_stock_actual, v_precio_unitario
        FROM productos 
        WHERE id = v_producto_id AND activo = TRUE;
        
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Error: El producto con ID % no existe o está inactivo', v_producto_id;
        END IF;
        
        IF v_stock_actual < v_cantidad THEN
            RAISE EXCEPTION 'Error: Stock insuficiente. Stock disponible: %, Cantidad solicitada: %', 
                v_stock_actual, v_cantidad;
        END IF;
        
        RAISE NOTICE '✓ Stock validado: Producto ID %, Stock disponible: %, Solicitado: %', 
            v_producto_id, v_stock_actual, v_cantidad;

        -- =====================================================
        -- PASO 3: CREAR LA FACTURA CON EL USUARIO RELACIONADO
        -- =====================================================
        
        -- Generar número de factura único
        v_numero_factura := 'FAC-' || TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD-HH24MISS') || '-' || v_usuario_id;
        
        -- Calcular totales
        v_subtotal := v_precio_unitario * v_cantidad;
        v_impuestos := v_subtotal * 0.13; -- 13% de impuestos (ejemplo Costa Rica)
        v_total := v_subtotal + v_impuestos;
        
        -- Insertar factura
        INSERT INTO facturas (numero_factura, usuario_id, subtotal, impuestos, total, estado)
        VALUES (v_numero_factura, v_usuario_id, v_subtotal, v_impuestos, v_total, 'PENDIENTE')
        RETURNING id INTO v_factura_id;
        
        RAISE NOTICE '✓ Factura creada: ID %, Número: %, Total: %', v_factura_id, v_numero_factura, v_total;

        -- Insertar detalle de factura
        INSERT INTO detalle_facturas (factura_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (v_factura_id, v_producto_id, v_cantidad, v_precio_unitario, v_subtotal);
        
        RAISE NOTICE '✓ Detalle de factura agregado: Producto ID %, Cantidad: %', v_producto_id, v_cantidad;

        -- =====================================================
        -- PASO 4: REDUCIR EL STOCK DEL PRODUCTO
        -- =====================================================
        UPDATE productos 
        SET stock = stock - v_cantidad
        WHERE id = v_producto_id;
        
        RAISE NOTICE '✓ Stock actualizado: Producto ID %, Nuevo stock: %', v_producto_id, (v_stock_actual - v_cantidad);

        -- =====================================================
        -- TRANSACCIÓN COMPLETADA EXITOSAMENTE
        -- =====================================================
        RAISE NOTICE '=== TRANSACCIÓN COMPLETADA EXITOSAMENTE ===';
        RAISE NOTICE 'Factura: % | Total: $ % | Stock restante: %', 
            v_numero_factura, v_total, (v_stock_actual - v_cantidad);

    EXCEPTION
        WHEN OTHERS THEN
            -- En caso de cualquier error, se hace rollback automático
            RAISE NOTICE '❌ ERROR EN LA TRANSACCIÓN: %', SQLERRM;
            RAISE NOTICE '❌ Todos los cambios han sido revertidos (ROLLBACK)';
            RAISE; -- Re-lanza la excepción para que se vea el error
    END;
END $$;

-- =====================================================
-- CONSULTAS PARA VERIFICAR LOS RESULTADOS
-- =====================================================

-- Verificar la última factura creada
SELECT 
    f.id,
    f.numero_factura,
    u.nombre as nombre_usuario,
    f.fecha_factura,
    f.subtotal,
    f.impuestos,
    f.total,
    f.estado
FROM facturas f 
JOIN usuarios u ON f.usuario_id = u.id 
ORDER BY f.fecha_factura DESC 
LIMIT 1;

-- Verificar el detalle de la última factura
SELECT 
    df.cantidad,
    df.precio_unitario,
    df.subtotal,
    p.nombre as nombre_producto,
    p.stock as stock_actual
FROM detalle_facturas df 
JOIN productos p ON df.producto_id = p.id 
JOIN facturas f ON df.factura_id = f.id 
ORDER BY f.fecha_factura DESC
LIMIT 1;

-- Verificar el stock actualizado del producto
SELECT 
    id, 
    nombre, 
    precio,
    stock,
    categoria
FROM productos 
WHERE id = 1; -- Cambiar por el ID del producto comprado

-- =====================================================
-- EJEMPLO DE TRANSACCIÓN CON MANEJO DE ERRORES
-- =====================================================

-- Ejemplo que falla por stock insuficiente
DO $$
DECLARE
    v_usuario_id INTEGER := 1;
    v_producto_id INTEGER := 1;
    v_cantidad INTEGER := 1000; -- Cantidad que excede el stock
BEGIN
    BEGIN
        RAISE NOTICE '=== PROBANDO TRANSACCIÓN CON ERROR (Stock insuficiente) ===';
        
        -- Intentar compra con stock insuficiente
        -- (Aquí iría el mismo código de la transacción principal)
        
        -- Validar stock
        IF (SELECT stock FROM productos WHERE id = v_producto_id) < v_cantidad THEN
            RAISE EXCEPTION 'Stock insuficiente para la compra';
        END IF;
        
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE '❌ Error esperado: %', SQLERRM;
            RAISE NOTICE '✓ La transacción se revirtió correctamente';
    END;
END $$;
