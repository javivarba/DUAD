-- Script para confirmar devolución y completar alquiler
SET search_path = lyfter_car_rental;

-- Ejemplo: Completar alquiler con ID 1
-- Primero verificar el alquiler activo
SELECT 
    r.id as rental_id,
    u.nombre as usuario,
    c.marca || ' ' || c.modelo as vehiculo,
    r.fecha_alquiler,
    r.fecha_devolucion_estimada,
    r.estado_alquiler,
    c.estado_automovil
FROM rentals r
JOIN users u ON r.user_id = u.id
JOIN cars c ON r.car_id = c.id
WHERE r.id = 1 AND r.estado_alquiler = 'activo';

-- Actualizar el alquiler como completado
UPDATE rentals 
SET 
    estado_alquiler = 'completado',
    fecha_devolucion_real = CURRENT_DATE,
    observaciones = COALESCE(observaciones, '') || ' | Devolución completada el ' || CURRENT_DATE
WHERE id = 1 AND estado_alquiler = 'activo';

-- Obtener el car_id del alquiler para actualizar su estado
-- Actualizar estado del automóvil a disponible
UPDATE cars 
SET estado_automovil = 'disponible'
WHERE id = (
    SELECT car_id 
    FROM rentals 
    WHERE id = 1
);

-- Verificar que todo se actualizó correctamente
SELECT 
    r.id as rental_id,
    u.nombre as usuario,
    c.marca || ' ' || c.modelo as vehiculo,
    r.fecha_alquiler,
    r.fecha_devolucion_estimada,
    r.fecha_devolucion_real,
    r.estado_alquiler,
    c.estado_automovil,
    CASE 
        WHEN r.fecha_devolucion_real <= r.fecha_devolucion_estimada 
        THEN 'A tiempo' 
        ELSE 'Con retraso' 
    END as puntualidad
FROM rentals r
JOIN users u ON r.user_id = u.id
JOIN cars c ON r.car_id = c.id
WHERE r.id = 1;

SELECT 'Devolución procesada y alquiler completado exitosamente' as resultado;