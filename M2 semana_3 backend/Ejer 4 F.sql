-- SQLite
SELECT 
    numero_factura,
    fecha_compra,
    correo_comprador,
    telefono_comprador,
    codigo_empleado_cajero,
    monto_total
FROM facturas
ORDER BY monto_total DESC;