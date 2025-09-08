-- Script para agregar un automóvil nuevo
SET search_path = lyfter_car_rental;

-- Agregar nuevo automóvil
INSERT INTO cars (marca, modelo, ano_fabricacion, estado_automovil) 
VALUES (
    'Tesla', 
    'Model 3', 
    2024, 
    'disponible'
);

-- Verificar que se agregó correctamente
SELECT 
    id, 
    marca, 
    modelo, 
    ano_fabricacion, 
    estado_automovil,
    fecha_registro
FROM cars 
WHERE marca = 'Tesla' AND modelo = 'Model 3'
ORDER BY id DESC 
LIMIT 1;

-- Mostrar mensaje de confirmación
SELECT 'Automóvil agregado exitosamente' as resultado;