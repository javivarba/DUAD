-- Script para cambiar el estado de un usuario
SET search_path = lyfter_car_rental;

-- Ejemplo: Cambiar estado del usuario con ID 5
-- Primero verificamos el estado actual
SELECT 
    id, 
    nombre, 
    username, 
    estado_cuenta as estado_actual
FROM users 
WHERE id = 5;

-- Cambiar el estado (si está activo lo desactivamos, si está inactivo lo activamos)
UPDATE users 
SET estado_cuenta = NOT estado_cuenta
WHERE id = 5;

-- Verificar el cambio
SELECT 
    id, 
    nombre, 
    username, 
    estado_cuenta as nuevo_estado,
    CASE 
        WHEN estado_cuenta = true THEN 'Activo' 
        ELSE 'Inactivo' 
    END as estado_descripcion
FROM users 
WHERE id = 5;

-- Mensaje de confirmación
SELECT 'Estado de usuario actualizado exitosamente' as resultado;