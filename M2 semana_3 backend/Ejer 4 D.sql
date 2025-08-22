-- SQLite
SELECT 
    p.codigo,
    p.nombre as producto,
    p.precio as precio_unitario,
    COUNT(fp.numero_factura) as total_facturas,
    SUM(fp.cantidad) as cantidad_total_vendida,
    SUM(fp.monto_parcial) as monto_total_vendido,
    ROUND(AVG(fp.cantidad), 2) as promedio_cantidad_por_factura
FROM productos p
LEFT JOIN factura_productos fp ON p.codigo = fp.codigo_producto
GROUP BY p.codigo, p.nombre, p.precio
ORDER BY monto_total_vendido DESC;