-- Script para obtener todos los automóviles disponibles
SET search_path = lyfter_car_rental;

-- Consulta principal: Automóviles disponibles para alquiler
SELECT 
    c.id as car_id,
    c.marca,
    c.modelo,
    c.ano_fabricacion,
    c.estado_automovil,
    c.fecha_registro,
    -- Información del último alquiler (si existe)
    last_rental.fecha_devolucion_real as ultima_devolucion,
    last_rental.cliente_anterior,
    CASE 
        WHEN c.ano_fabricacion >= 2023 THEN 'Nuevo'
        WHEN c.ano_fabricacion >= 2020 THEN 'Reciente'
        ELSE 'Estándar'
    END as categoria_vehiculo
FROM cars c
LEFT JOIN (
    SELECT DISTINCT ON (r.car_id)
        r.car_id,
        r.fecha_devolucion_real,
        u.nombre as cliente_anterior
    FROM rentals r
    JOIN users u ON r.user_id = u.id
    WHERE r.estado_alquiler = 'completado'
    ORDER BY r.car_id, r.fecha_devolucion_real DESC
) last_rental ON c.id = last_rental.car_id
WHERE c.estado_automovil = 'disponible'
ORDER BY c.marca, c.modelo, c.ano_fabricacion DESC;

-- Resumen de automóviles disponibles
SELECT 
    COUNT(*) as total_disponibles,
    COUNT(CASE WHEN ano_fabricacion >= 2023 THEN 1 END) as nuevos_2023_plus,
    COUNT(CASE WHEN ano_fabricacion BETWEEN 2020 AND 2022 THEN 1 END) as recientes_2020_2022,
    COUNT(CASE WHEN ano_fabricacion < 2020 THEN 1 END) as estandar_pre_2020,
    ROUND(AVG(ano_fabricacion), 1) as ano_promedio
FROM cars 
WHERE estado_automovil = 'disponible';

-- Automóviles disponibles agrupados por marca
SELECT 
    marca,
    COUNT(*) as cantidad_disponible,
    MIN(ano_fabricacion) as ano_mas_antiguo,
    MAX(ano_fabricacion) as ano_mas_nuevo,
    ROUND(AVG(ano_fabricacion), 1) as ano_promedio
FROM cars 
WHERE estado_automovil = 'disponible'
GROUP BY marca
ORDER BY cantidad_disponible DESC;

-- Top 10 modelos disponibles más nuevos
SELECT 
    marca || ' ' || modelo as vehiculo_completo,
    ano_fabricacion,
    fecha_registro,
    id as car_id
FROM cars 
WHERE estado_automovil = 'disponible'
ORDER BY ano_fabricacion DESC, fecha_registro DESC
LIMIT 10;