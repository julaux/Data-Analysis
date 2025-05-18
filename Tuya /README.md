# PRUEBA ANALISTA DE DATOS - JULIAN AUX

## **Fase 1: Extracción y Combinación de Datos**

Se cuenta con un modelo relacional de base de datos, la cual consta de cinco tablas interconectadas así:

**Tablas**
1. cliente: cedula (PK), nombre y telefono.
2. proveedor: id_proveedor (PK), nombre y telefono.
3. orden: id_orden (PK), nor_orden, cedula (FK), fecha_orden, total_pedido.
4. producto: id_producto (PK), nombre_producto, id_proveedor (FK), precio_unitario, activo_sn.
5. detalle_orden: id_orden (FK), id_producto (FK), precio_unitario, cantidad.

### Preguntas

1. Número total de ordenes registradas.

R/
SELECT COUNT(*) AS total_ordenes
FROM orden;

2. Número de clientes que han realizado órdenes entre el 01-01-2021 y la fecha actual.
   
R/

SELECT COUNT(DISTINCT o.cedula) AS total_clientes
FROM orden o
WHERE o.fecha_orden BETWEEN '2021-01-01' AND CURRENT_DATE;

3. Listado total de clientes con la cantidad total de órdenes realizadas (conteo), ordenando de mayor a menor nro. de órdenes
R/
SELECT c.nombre AS cliente, COUNT(o.id_orden) AS total_ordenes
FROM cliente c
JOIN orden o ON c.cedula = o.cedula
GROUP BY c.cedula
ORDER BY total_ordenes DESC;

4. Detalle completo (datos del cliente, fecha, nombre producto, cantidad) del pedido cuyo monto fue el más grande (en valor, no en unidades) en el año 2020. 
R/
SELECT 
    c.nombre AS cliente, 
    o.fecha_orden, 
    p.nombre_producto, 
    d.cantidad, 
    (d.precio_unitario * d.cantidad) AS monto_producto
FROM cliente c
JOIN orden o ON c.cedula = o.cedula
JOIN detalle_orden d ON o.id_orden = d.id_orden
JOIN producto p ON d.id_producto = p.id_producto
WHERE o.fecha_orden BETWEEN '2020-01-01' AND '2020-12-31'
ORDER BY (d.precio_unitario * d.cantidad) DESC
LIMIT 1;

5. Valor total vendido por mes y año.
R/ 
SELECT 
    EXTRACT(YEAR FROM o.fecha_orden) AS anio,
    EXTRACT(MONTH FROM o.fecha_orden) AS mes,
    SUM(d.precio_unitario * d.cantidad) AS total_vendido
FROM orden o
JOIN detalle_orden d ON o.id_orden = d.id_orden
WHERE o.fecha_orden BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY EXTRACT(YEAR FROM o.fecha_orden), EXTRACT(MONTH FROM o.fecha_orden)
ORDER BY anio, mes;

6. Para el cliente con cédula 123456, especificar para cada producto, el número de veces que lo ha comprado y el valor total gastado en dicho producto. 
Ordenar el resultado de mayor a menor.
R/
SELECT 
    p.nombre_producto,
    COUNT(d.id_orden) AS veces_comprado,
    SUM(d.precio_unitario * d.cantidad) AS total_gastado
FROM cliente c
JOIN orden o ON c.cedula = o.cedula
JOIN detalle_orden d ON o.id_orden = d.id_orden
JOIN producto p ON d.id_producto = p.id_producto
WHERE c.cedula = '123456'
GROUP BY p.id_producto
ORDER BY total_gastado DESC;
