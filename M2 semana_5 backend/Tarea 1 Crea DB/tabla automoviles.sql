-- Script para crear y popular tabla de automóviles
-- Usar el schema
SET search_path = lyfter_car_rental;

-- Crear tabla de automóviles
CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(100) NOT NULL,
    ano_fabricacion INTEGER NOT NULL CHECK (ano_fabricacion >= 1900 AND ano_fabricacion <= EXTRACT(YEAR FROM CURRENT_DATE)),
    estado_automovil VARCHAR(20) DEFAULT 'disponible' CHECK (estado_automovil IN ('disponible', 'alquilado', 'mantenimiento', 'fuera_servicio')),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Popular tabla con automóviles variados
INSERT INTO cars (marca, modelo, ano_fabricacion, estado_automovil) VALUES
('Toyota', 'Corolla', 2022, 'disponible'),
('Honda', 'Civic', 2023, 'disponible'),
('Ford', 'Focus', 2021, 'alquilado'),
('Chevrolet', 'Cruze', 2022, 'disponible'),
('Nissan', 'Sentra', 2023, 'disponible'),
('Hyundai', 'Elantra', 2021, 'mantenimiento'),
('Volkswagen', 'Jetta', 2022, 'disponible'),
('Mazda', 'Mazda3', 2023, 'alquilado'),
('Kia', 'Forte', 2021, 'disponible'),
('Subaru', 'Impreza', 2022, 'disponible'),
('BMW', 'Serie 3', 2023, 'disponible'),
('Mercedes-Benz', 'Clase A', 2022, 'alquilado'),
('Audi', 'A3', 2023, 'disponible'),
('Toyota', 'RAV4', 2022, 'disponible'),
('Honda', 'CR-V', 2023, 'mantenimiento'),
('Ford', 'Escape', 2021, 'disponible'),
('Chevrolet', 'Equinox', 2022, 'disponible'),
('Nissan', 'X-Trail', 2023, 'alquilado'),
('Hyundai', 'Tucson', 2021, 'disponible'),
('Volkswagen', 'Tiguan', 2022, 'disponible'),
('Mazda', 'CX-5', 2023, 'disponible'),
('Kia', 'Sportage', 2022, 'fuera_servicio'),
('Subaru', 'Forester', 2021, 'disponible'),
('BMW', 'X1', 2023, 'disponible'),
('Mercedes-Benz', 'GLA', 2022, 'alquilado'),
('Audi', 'Q3', 2023, 'disponible'),
('Toyota', 'Camry', 2022, 'disponible'),
('Honda', 'Accord', 2023, 'mantenimiento'),
('Ford', 'Fusion', 2021, 'disponible'),
('Chevrolet', 'Malibu', 2022, 'disponible'),
('Nissan', 'Altima', 2023, 'disponible'),
('Hyundai', 'Sonata', 2021, 'alquilado'),
('Volkswagen', 'Passat', 2022, 'disponible'),
('Mazda', 'Mazda6', 2023, 'disponible'),
('Kia', 'K5', 2022, 'disponible'),
('Subaru', 'Legacy', 2021, 'mantenimiento'),
('BMW', 'Serie 5', 2023, 'disponible'),
('Mercedes-Benz', 'Clase C', 2022, 'disponible'),
('Audi', 'A4', 2023, 'alquilado'),
('Toyota', 'Highlander', 2022, 'disponible'),
('Honda', 'Pilot', 2023, 'disponible'),
('Ford', 'Explorer', 2021, 'fuera_servicio'),
('Chevrolet', 'Traverse', 2022, 'disponible'),
('Nissan', 'Pathfinder', 2023, 'disponible'),
('Hyundai', 'Palisade', 2021, 'mantenimiento'),
('Volkswagen', 'Atlas', 2022, 'disponible'),
('Mazda', 'CX-9', 2023, 'disponible'),
('Kia', 'Sorento', 2022, 'alquilado'),
('Subaru', 'Ascent', 2021, 'disponible'),
('BMW', 'X5', 2023, 'disponible'),
('Mercedes-Benz', 'GLE', 2022, 'disponible');

-- Verificar inserción
SELECT COUNT(*) as total_autos, estado_automovil, COUNT(*) as cantidad
FROM cars 
GROUP BY estado_automovil;