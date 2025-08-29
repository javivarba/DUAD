-- Script para generar un alquiler nuevo
SET search_path = lyfter_car_rental;

-- Variables para el nuevo alquiler (cambiar según necesidades)
-- Usuario ID: 10, Automóvil ID: 5, 7 días de alquiler

-- Verificar que el usuario existe y está activo
SELECT 
    id, 
    nombre, 
    estado_cuenta
FROM users 
WHERE id = 10 AND estado_cuenta = true;

-- Verificar que el automóvil existe y está disponible
SELECT 
    id, 
    marca, 
    modelo, 
    estado_automovil
FROM cars 
WHERE id = 5 AND estado_automovil = 'disponible';

-- Solo proceder si ambas verificaciones son exitosas
-- Crear el alquiler
INSERT INTO rentals (
    user_id, 
    car_id, 
    fecha_alquiler, 
    fecha_devolucion_estimada, 
    estado_alquiler, 
    precio_total, 
    observaciones
) VALUES (
    10,                                              -- user_id
    5,                                               -- car_id
    CURRENT_TIMESTAMP,                               -- fecha_alquiler (automática)
    CURRENT_DATE + INTERVAL '7 days',               -- fecha_devolucion_estimada (7 días)
    'activo',                                        -- estado_alquiler
    245.00,                                          -- precio_total (7 días x $35/día)
    'Alquiler generado por script de prueba'        -- observaciones
);

-- Actualizar estado del automóvil a alquilado
UPDATE cars 
SET estado_automovil = 'alquilado'
WHERE id = 5;

-- Verificar el alquiler creado
SELECT 
    r.id as rental_id,
    u.nombre as usuario,
    c.marca || ' ' || c.modelo as vehiculo,
    r.fecha_alquiler,
    r.fecha_devolucion_estimada,
    r.estado_alquiler,
    r.precio_total,
    c.estado_automovil as estado_auto
FROM rentals r
JOIN users u ON r.user_id = u.id
JOIN cars c ON r.car_id = c.id
WHERE r.user_id = 10 AND r.car_id = 5
ORDER BY r.id DESC
LIMIT 1;

SELECT 'Alquiler creado exitosamente' as resultado;