-- Script para agregar un usuario nuevo
SET search_path = lyfter_car_rental;

-- Agregar nuevo usuario con validaciones
INSERT INTO users (nombre, correo, username, password, fecha_nacimiento, estado_cuenta) 
VALUES (
    'Juan Pérez Nuevos', 
    'juan.perez.nuevo@email.com', 
    'jperezn', 
    'password123!', 
    '1995-06-15', 
    true
);

-- Verificar que se agregó correctamente
SELECT 
    id, 
    nombre, 
    correo, 
    username, 
    estado_cuenta,
    fecha_creacion
FROM users 
WHERE correo = 'juan.perez.nuevo@email.com';

-- Mostrar mensaje de confirmación
SELECT 'Usuario agregado exitosamente' as resultado;