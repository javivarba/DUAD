-- Script para crear tabla de alquileres (tabla cruz)
-- Usar el schema
SET search_path = lyfter_car_rental;

-- Crear tabla de alquileres
CREATE TABLE IF NOT EXISTS rentals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    fecha_alquiler TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion_estimada DATE,
    fecha_devolucion_real DATE,
    estado_alquiler VARCHAR(20) DEFAULT 'activo' CHECK (estado_alquiler IN ('activo', 'completado', 'cancelado', 'en_mora')),
    precio_total DECIMAL(10,2),
    observaciones TEXT,
    
    -- Claves foráneas
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
    
    -- Índices para mejorar rendimiento
    CONSTRAINT unique_active_rental UNIQUE (car_id, estado_alquiler) 
    DEFERRABLE INITIALLY DEFERRED
);

-- Remover constraint que impide múltiples alquileres del mismo auto
ALTER TABLE rentals DROP CONSTRAINT IF EXISTS unique_active_rental;

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_rentals_user_id ON rentals(user_id);
CREATE INDEX IF NOT EXISTS idx_rentals_car_id ON rentals(car_id);
CREATE INDEX IF NOT EXISTS idx_rentals_estado ON rentals(estado_alquiler);
CREATE INDEX IF NOT EXISTS idx_rentals_fecha ON rentals(fecha_alquiler);

-- Popular tabla con alquileres de ejemplo
INSERT INTO rentals (user_id, car_id, fecha_alquiler, fecha_devolucion_estimada, fecha_devolucion_real, estado_alquiler, precio_total, observaciones) VALUES
(1, 3, '2024-08-01 10:30:00', '2024-08-08', NULL, 'activo', 350.00, 'Cliente regular, sin observaciones'),
(5, 8, '2024-08-05 14:15:00', '2024-08-12', NULL, 'activo', 420.00, 'Alquiler de larga duración'),
(12, 18, '2024-07-28 09:20:00', '2024-08-04', '2024-08-04', 'completado', 280.00, 'Devolución puntual'),
(18, 25, '2024-08-10 16:45:00', '2024-08-15', NULL, 'activo', 500.00, 'Vehículo premium'),
(23, 32, '2024-07-15 11:30:00', '2024-07-22', '2024-07-23', 'completado', 315.00, 'Devolución con un día de retraso'),
(7, 39, '2024-08-12 13:00:00', '2024-08-19', NULL, 'activo', 385.00, 'Primera vez del cliente'),
(33, 47, '2024-07-20 08:45:00', '2024-07-25', NULL, 'en_mora', 225.00, 'Cliente no ha devuelto el vehículo'),
(41, 12, '2024-08-03 15:20:00', '2024-08-10', '2024-08-09', 'completado', 295.00, 'Sin problemas'),
(15, 6, '2024-08-08 12:10:00', '2024-08-13', NULL, 'activo', 180.00, 'Alquiler económico'),
(28, 29, '2024-07-25 17:30:00', '2024-08-01', '2024-08-01', 'completado', 340.00, 'Cliente frecuente'),
(3, 41, '2024-08-14 10:00:00', '2024-08-21', NULL, 'activo', 450.00, 'Alquiler para vacaciones'),
(45, 22, '2024-07-30 14:25:00', '2024-08-06', NULL, 'cancelado', 0.00, 'Cliente canceló por emergencia'),
(9, 35, '2024-08-06 09:15:00', '2024-08-13', NULL, 'activo', 375.00, 'Requiere asiento para niños'),
(37, 15, '2024-08-02 16:40:00', '2024-08-09', '2024-08-08', 'completado', 320.00, 'Entrega anticipada'),
(21, 44, '2024-08-11 11:55:00', '2024-08-18', NULL, 'activo', 290.00, 'Sin observaciones especiales'),
(50, 9, '2024-07-18 13:45:00', '2024-07-25', '2024-07-26', 'completado', 265.00, 'Pequeño retraso en devolución'),
(11, 26, '2024-08-09 08:30:00', '2024-08-16', NULL, 'activo', 410.00, 'Vehículo SUV solicitado'),
(39, 37, '2024-08-07 15:10:00', '2024-08-14', NULL, 'activo', 360.00, 'Cliente corporativo'),
(25, 50, '2024-07-22 12:20:00', '2024-07-29', NULL, 'en_mora', 480.00, 'No responde a llamadas'),
(17, 14, '2024-08-13 14:50:00', '2024-08-20', NULL, 'activo', 325.00, 'Conductor adicional autorizado');

-- Verificar los datos insertados
SELECT 
    estado_alquiler, 
    COUNT(*) as cantidad,
    AVG(precio_total) as precio_promedio
FROM rentals 
GROUP BY estado_alquiler
ORDER BY cantidad DESC;