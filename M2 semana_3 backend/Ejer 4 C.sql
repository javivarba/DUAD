-- SQLite
SELECT 
    fp.numero_factura,
    f.fecha_compra,
    f.correo_comprador,
    p.nombre as producto,
    p.codigo as codigo_producto,
    fp.cantidad,
    p.precio as precio_unitario,
    fp.monto_parcial
FROM factura_productos fp
JOIN facturas f ON fp.numero_factura = f.numero_factura
JOIN productos p ON fp.codigo_producto = p.codigo
WHERE p.codigo = 'P003'
ORDER BY f.fecha_compra;