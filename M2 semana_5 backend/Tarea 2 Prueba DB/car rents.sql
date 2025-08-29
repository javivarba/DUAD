-- Script para obtener todos los automóviles alquilados
SET search_path = lyfter_car_rental;

-- Consulta principal: Automóviles con alquileres activos
SELECT 
    c.id as car_id,
    c.marca,
    c.modelo,
    c.ano_fabricacion,
    c.estado_automovil,
    r.id as rental_id,
    u.nombre as cliente,
    u.username as cliente_username,
    r.fecha_alquiler,
    r.fecha_devolucion_estimada,
    r.precio_total,
    CASE 
        WHEN r.fecha_devolucion_estimada < CURRENT_DATE 
        THEN 'En mora'
        WHEN r.fecha_devolucion_estimada = CURRENT_DATE 
        THEN 'Vence hoy'
        ELSE 'Vigente'
    END as estado_devolucion,
    r.observaciones
FROM cars c
INNER JOIN rentals r ON c.id = r.car_id
INNER JOIN users u ON r.user_id = u.id
WHERE r.estado_alquiler = 'activo'
ORDER BY r.fecha_devolucion_estimada ASC;

-- Resumen estadístico de automóviles alquilados
SELECT 
    COUNT(*) as total_alquilados,
    COUNT(CASE WHEN r.fecha_devolucion_estimada < CURRENT_DATE THEN 1 END) as en_mora,
    COUNT(CASE WHEN r.fecha_devolucion_estimada = CURRENT_DATE THEN 1 END) as vencen_hoy,
    COUNT(CASE WHEN r.fecha_devolucion_estimada > CURRENT_DATE THEN 1 END) as vigentes,
    AVG(r.precio_total) as precio_promedio
FROM cars c
INNER JOIN rentals r ON c.id = r.car_id
WHERE r.estado_alquiler = 'activo';

-- Automóviles alquilados por marca
SELECT 
    c.marca,
    COUNT(*) as cantidad_alquilada,
    AVG(r.precio_total) as precio_promedio_marca
FROM cars c
INNER JOIN rentals r ON c.id = r.car_id
WHERE r.estado_alquiler = 'activo'
GROUP BY c.marca
ORDER BY cantidad_alquilada DESC;