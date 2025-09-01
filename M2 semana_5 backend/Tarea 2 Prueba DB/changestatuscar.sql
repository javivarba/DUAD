-- Script para cambiar el estado de un automóvil
SET search_path = lyfter_car_rental;

-- Ejemplo: Cambiar estado del automóvil con ID 10
-- Primero verificamos el estado actual
SELECT 
    id, 
    marca, 
    modelo, 
    estado_automovil as estado_actual
FROM cars 
WHERE id = 10;

-- Cambiar estado a mantenimiento
UPDATE cars 
SET estado_automovil = 'mantenimiento'
WHERE id = 10;

-- Verificar el cambio
SELECT 
    id, 
    marca, 
    modelo, 
    estado_automovil as nuevo_estado
FROM cars 
WHERE id = 10;

-- Script adicional para cambiar a cualquier estado válido
-- Descomenta y modifica según necesites:

-- Para poner disponible:
-- UPDATE cars SET estado_automovil = 'disponible' WHERE id = 10;

-- Para poner alquilado:
-- UPDATE cars SET estado_automovil = 'alquilado' WHERE id = 10;

-- Para poner fuera de servicio:
-- UPDATE cars SET estado_automovil = 'fuera_servicio' WHERE id = 10;

SELECT 'Estado de automóvil actualizado exitosamente' as resultado;