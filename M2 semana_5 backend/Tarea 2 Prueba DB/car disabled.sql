-- Script para deshabilitar un automóvil del alquiler
SET search_path = lyfter_car_rental;

-- Ejemplo: Deshabilitar automóvil con ID 15
-- Primero verificar el estado actual y si tiene alquileres activos
SELECT 
    c.id,
    c.marca,
    c.modelo,
    c.estado_automovil,
    COUNT(r.id) as alquileres_activos
FROM cars c
LEFT JOIN rentals r ON c.id = r.car_id AND r.estado_alquiler = 'activo'
WHERE c.id = 15
GROUP BY c.id, c.marca, c.modelo, c.estado_automovil;

-- Si el automóvil tiene alquileres activos, mostrar advertencia
SELECT 
    CASE 
        WHEN COUNT(*) > 0 
        THEN 'ADVERTENCIA: Este automóvil tiene alquileres activos'
        ELSE 'OK: Automóvil puede ser deshabilitado'
    END as verificacion
FROM rentals 
WHERE car_id = 15 AND estado_alquiler = 'activo';

-- Opción 1: Deshabilitar forzadamente (usar con cuidado)
-- Esto cancela alquileres activos automáticamente
UPDATE rentals 
SET 
    estado_alquiler = 'cancelado',
    observaciones = COALESCE(observaciones, '') || ' | Cancelado por deshabilitación del vehículo - ' || CURRENT_DATE
WHERE car_id = 15 AND estado_alquiler = 'activo';

-- Cambiar estado del automóvil a fuera de servicio
UPDATE cars 
SET estado_automovil = 'fuera_servicio'
WHERE id = 15;

-- Opción 2: Solo cambiar estado si no hay alquileres activos (más seguro)
-- Descomenta estas líneas si prefieres este enfoque:

-- UPDATE cars 
-- SET estado_automovil = 'fuera_servicio'
-- WHERE id = 15 
-- AND NOT EXISTS (
--     SELECT 1 FROM rentals 
--     WHERE car_id = 15 AND estado_alquiler = 'activo'
-- );

-- Verificar el resultado
SELECT 
    c.id,
    c.marca || ' ' || c.modelo as vehiculo,
    c.estado_automovil,
    COUNT(CASE WHEN r.estado_alquiler = 'activo' THEN 1 END) as alquileres_activos,
    COUNT(CASE WHEN r.estado_alquiler = 'cancelado' THEN 1 END) as alquileres_cancelados
FROM cars c
LEFT JOIN rentals r ON c.id = r.car_id
WHERE c.id = 15
GROUP BY c.id, c.marca, c.modelo, c.estado_automovil;

SELECT 'Automóvil deshabilitado del servicio de alquiler' as resultado;