-- Script para crear y popular tabla de usuarios
-- Ejecutar todo de una vez

-- Usar el schema creado
SET search_path = lyfter_car_rental;

-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    estado_cuenta BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Popular tabla con 50 usuarios
INSERT INTO users (nombre, correo, username, password, fecha_nacimiento, estado_cuenta) VALUES
('Ana García López', 'ana.garcia@email.com', 'anagl', 'pass123!', '1990-03-15', true),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', 'carlosrod', 'secure456', '1985-07-22', true),
('María Fernández', 'maria.fernandez@email.com', 'mariaf', 'mypass789', '1992-11-08', true),
('José Martínez', 'jose.martinez@email.com', 'jmartinez', 'password01', '1988-05-30', false),
('Laura Sánchez', 'laura.sanchez@email.com', 'lauras', 'secret123', '1995-01-12', true),
('Roberto Chen', 'roberto.chen@email.com', 'rchen', 'pass2024', '1987-09-18', true),
('Carmen Jiménez', 'carmen.jimenez@email.com', 'carmenj', 'mykey456', '1991-04-25', true),
('Daniel Torres', 'daniel.torres@email.com', 'dtorres', 'secure789', '1989-12-03', true),
('Isabel Morales', 'isabel.morales@email.com', 'imorales', 'password2', '1993-08-14', false),
('Miguel Ángel Vega', 'miguel.vega@email.com', 'mvega', 'strong123', '1986-06-27', true),
('Patricia Ruiz', 'patricia.ruiz@email.com', 'pruiz', 'mypass01', '1994-02-09', true),
('Fernando Castro', 'fernando.castro@email.com', 'fcastro', 'secure2024', '1983-10-16', true),
('Claudia Herrera', 'claudia.herrera@email.com', 'cherrera', 'password99', '1990-12-21', true),
('Ricardo Mendoza', 'ricardo.mendoza@email.com', 'rmendoza', 'key123456', '1988-03-07', false),
('Gabriela Silva', 'gabriela.silva@email.com', 'gsilva', 'pass4567', '1992-07-19', true),
('Alejandro Ramos', 'alejandro.ramos@email.com', 'aramos', 'secure890', '1985-11-11', true),
('Mónica Delgado', 'monica.delgado@email.com', 'mdelgado', 'mypass234', '1991-05-28', true),
('Sergio Ortega', 'sergio.ortega@email.com', 'sortega', 'password67', '1989-01-15', true),
('Verónica Campos', 'veronica.campos@email.com', 'vcampos', 'strong567', '1993-09-02', false),
('Andrés Gutiérrez', 'andres.gutierrez@email.com', 'agutierrez', 'secure345', '1987-04-13', true),
('Natalia Vargas', 'natalia.vargas@email.com', 'nvargas', 'mykey789', '1995-08-26', true),
('Diego Peña', 'diego.pena@email.com', 'dpena', 'pass890123', '1984-12-08', true),
('Lorena Aguilar', 'lorena.aguilar@email.com', 'laguilar', 'password45', '1990-06-17', true),
('Javier Romero', 'javier.romero@email.com', 'jromero', 'secure678', '1988-10-24', false),
('Silvia Navarro', 'silvia.navarro@email.com', 'snavarro', 'mypass567', '1992-02-11', true),
('Hugo Paredes', 'hugo.paredes@email.com', 'hparedes', 'strong890', '1986-07-29', true),
('Elena Ibáñez', 'elena.ibanez@email.com', 'eibanez', 'password78', '1994-11-16', true),
('Óscar Luna', 'oscar.luna@email.com', 'oluna', 'secure456789', '1989-03-23', true),
('Beatriz Moreno', 'beatriz.moreno@email.com', 'bmoreno', 'mypass890', '1991-09-05', false),
('Raúl Cortés', 'raul.cortes@email.com', 'rcortes', 'key567890', '1987-01-18', true),
('Amparo Hidalgo', 'amparo.hidalgo@email.com', 'ahidalgo', 'password123', '1993-05-31', true),
('Iván Guerrero', 'ivan.guerrero@email.com', 'iguerrero', 'secure234567', '1985-08-14', true),
('Rosa Márquez', 'rosa.marquez@email.com', 'rmarquez', 'mypass456', '1990-12-27', true),
('Cristian Reyes', 'cristian.reyes@email.com', 'creyes', 'strong345', '1988-04-10', false),
('Esperanza Blanco', 'esperanza.blanco@email.com', 'eblanco', 'password67890', '1992-10-22', true),
('Manuel Pascual', 'manuel.pascual@email.com', 'mpascual', 'secure123456', '1984-06-05', true),
('Concepción Gil', 'concepcion.gil@email.com', 'cgil', 'mykey234', '1991-02-16', true),
('Tomás Ferrer', 'tomas.ferrer@email.com', 'tferrer', 'pass345678', '1989-08-28', true),
('Pilar Caballero', 'pilar.caballero@email.com', 'pcaballero', 'strong678', '1995-01-09', false),
('Francisco Gallego', 'francisco.gallego@email.com', 'fgallego', 'password890', '1987-05-21', true),
('Dolores Prieto', 'dolores.prieto@email.com', 'dprieto', 'secure789012', '1993-11-12', true),
('Antonio Cano', 'antonio.cano@email.com', 'acano', 'mypass678', '1986-03-25', true),
('Remedios Santos', 'remedios.santos@email.com', 'rsantos', 'key890123', '1990-07-07', true),
('Enrique Rubio', 'enrique.rubio@email.com', 'erubio', 'password234', '1988-11-19', false),
('Soledad Molina', 'soledad.molina@email.com', 'smolina', 'strong901', '1992-04-01', true),
('Ramón Iglesias', 'ramon.iglesias@email.com', 'riglesias', 'secure567890', '1985-09-13', true),
('Guadalupe Lozano', 'guadalupe.lozano@email.com', 'glozano', 'mypass345', '1994-01-26', true),
('Emilio Herrero', 'emilio.herrero@email.com', 'eherrero', 'password567', '1989-06-08', true),
('Inmaculada Cruz', 'inmaculada.cruz@email.com', 'icruz', 'strong234', '1991-12-20', false),
('Julián Núñez', 'julian.nunez@email.com', 'jnunez', 'secure890123', '1987-08-02', true);

-- Verificar que se insertaron los datos
SELECT COUNT(*) as total_usuarios FROM users;