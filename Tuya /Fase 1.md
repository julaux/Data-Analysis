# PRUEBA ANALISTA DE DATOS - JULIAN AUX

## **Fase 1: Extracción y Combinación de Datos**

Se cuenta con un modelo relacional de base de datos, que consta de las siguientes tablas interconectadas:

### **Tablas**
1. **cliente**: 
   - `cedula` (PK): Identificador único del cliente.
   - `nombre`: Nombre del cliente.
   - `telefono`: Teléfono del cliente (opcional).

2. **proveedor**: 
   - `id_proveedor` (PK): Identificador único del proveedor.
   - `nombre`: Nombre del proveedor.
   - `telefono`: Teléfono del proveedor (opcional).

3. **orden**:
   - `id_orden` (PK): Identificador único de la orden.
   - `nro_orden`: Número de orden (opcional).
   - `cedula` (FK): Relación con el cliente que hizo la orden.
   - `fecha_orden`: Fecha de la orden.
   - `total_pedido`: Monto total de la orden.

4. **producto**:
   - `id_producto` (PK): Identificador único del producto.
   - `nombre_producto`: Nombre del producto.
   - `id_proveedor` (FK): Relación con el proveedor del producto.
   - `precio_unitario`: Precio del producto (opcional).
   - `activo_sn`: Indicador de si el producto está activo (booleano).

5. **detalle_orden**:
   - `id_orden` (FK): Relación con la orden.
   - `id_producto` (FK): Relación con el producto.
   - `precio_unitario`: Precio del producto en esa orden.
   - `cantidad`: Cantidad pedida.

---

## **Consultas SQL**

### 1. Número total de órdenes registradas:
```sql
SELECT COUNT(*) AS total_ordenes
FROM orden;
```

### 2. Número de clientes que han realizado órdenes entre el 01-01-2021 y la fecha actual:
```sql
SELECT COUNT(DISTINCT o.cedula) AS total_clientes
FROM orden o
WHERE o.fecha_orden BETWEEN '2021-01-01' AND CURRENT_DATE;
```

### 3. Listado total de clientes con la cantidad total de órdenes realizadas (conteo), ordenando de mayor a menor nro. de órdenes:
```sql
SELECT c.nombre AS cliente, COUNT(o.id_orden) AS total_ordenes
FROM cliente c
JOIN orden o ON c.cedula = o.cedula
GROUP BY c.cedula
ORDER BY total_ordenes DESC;
```

### 4. Detalle completo (datos del cliente, fecha, nombre producto, cantidad) del pedido cuyo monto fue el más grande (en valor, no en unidades) en el año 2020. 
```sql
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
```

### 5. Valor total vendido por mes y año.
```sql
SELECT 
    EXTRACT(YEAR FROM o.fecha_orden) AS anio,
    EXTRACT(MONTH FROM o.fecha_orden) AS mes,
    SUM(d.precio_unitario * d.cantidad) AS total_vendido
FROM orden o
JOIN detalle_orden d ON o.id_orden = d.id_orden
WHERE o.fecha_orden BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY EXTRACT(YEAR FROM o.fecha_orden), EXTRACT(MONTH FROM o.fecha_orden)
ORDER BY anio, mes;
```

### 6. Para el cliente con cédula 123456, especificar para cada producto, el número de veces que lo ha comprado y el valor total gastado en dicho producto. Ordenar el resultado de mayor a menor.
```sql
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
```

### 7. Si necesitas actualizar una tabla histórica con los datos del último mes, y en este nuevo mes has incluido una nueva columna para la ciudad del cliente, ¿qué proceso seguirías para evitar conflictos por diferencia de dimensiones, considerando que no tienes acceso a los comandos ADD COLUMN o ALTER TABLE?
```sql
-- Proceso
-- 1. Crear una tabla temporal que tenga la nueva estructura, la cual incluye la columna 'ciudad' para el cliente.

CREATE TEMPORARY TABLE temp_ordenes_con_ciudad AS
SELECT o.*, c.ciudad
FROM orden o
JOIN cliente c ON o.cedula = c.cedula;

-- 2. Unir los datis históricos con los nuevos.

CREATE TABLE nueva_ordenes AS
SELECT * FROM orden;  -- copia de los datos históricos

-- actualización de la tabla nueva con la información de la tabla temporal
INSERT INTO nueva_ordenes
SELECT * FROM temp_ordenes_con_ciudad;

-- 3. Verificación y migración de los datos

DROP TABLE orden;  -- eliminación de la tabla antigua
RENAME nueva_ordenes TO orden; -- renombrar la nueva tabla
```
