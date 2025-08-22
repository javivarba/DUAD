-- SQLite
SELECT 
    codigo,
    nombre,
    precio,
    marca
FROM productos
WHERE precio > 5000
ORDER BY precio DESC;