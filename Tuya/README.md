# Análisis y Segmentación de Puntos de Venta

Este proyecto tiene como objetivo **analizar los puntos de venta** empleando **técnicas de aprendizaje no supervisado** para identificar patrones, segmentar los puntos de venta y generar estrategias basadas en datos para **optimizar el rendimiento**. A continuación, se describe el proceso paso a paso, dividido en cuatro fases.

## Fase 1: Extracción y Combinación de Datos

### Descripción:
En esta fase, se realizaron consultas SQL sobre una base de datos la cual contiene las tablas a continuación:

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


## Fase 2: Análisis de Información

### Descripción:
En esta fase, se utilizó el archivo **"Productividad.xlsx"** para realizar un análisis y determinar cuál era el **cargo más conveniente para contratar** con el fin de **incrementar la productividad**. Se consideraron los costos asociados a cada cargo:

- **Ejecutivo Comercial (Tiempo Completo)**: 100% del costo
- **Ejecutivo Comercial (Medio Tiempo)**: 50% del costo
- **Ejecutivo Comercial (Fines de Semana)**: 40% del costo

#### Análisis Realizado:
1. **Análisis Exploratorio de Datos (EDA)**:
   - Se realizó un **EDA completo** sobre el dataset **"Productividad.xlsx"** para entender las características de cada variable y detectar posibles relaciones.
   - Se determinó el número de **valores únicos** del campo **`cargobase`** para entender qué tipos de cargos están representados en los datos.
   - Se calcularon las **estadísticas de costo y productividad media** para cada tipo de cargo.
   
2. **Cálculo de Costo/Producto**:
   - Se calculó la **relación costo/productividad** para cada cargo, con el objetivo de evaluar qué cargo ofrece la **mejor eficiencia** en términos de costo por unidad de productividad.
   
3. **Análisis de Costo Promedio y Productividad Media**:
   - **Costo Promedio**: Se determinaron los costos promedios de cada cargo, teniendo en cuenta los **porcentajes de tiempo completo**, **medio tiempo** y **fines de semana**.
   - **Productividad Media**: Se calculó la **productividad media** de cada cargo, observando qué cargo tiene una mayor **productividad en relación con el costo**.

#### Gráficos:
Se realizaron varios **gráficos de barras** para comparar la **relación costo/productividad**, el **costo promedio** y la **productividad media** entre los diferentes cargos:

1. **Relación Costo/Productividad**: Muestra qué cargo tiene la **mejor relación costo-productividad**.
2. **Costo Promedio**: Compara los **costos promedio** de cada cargo.
3. **Productividad Media**: Muestra cuál cargo tiene la **mayor productividad media**.

#### Resultados:
1. **La mejor productividad media** la tiene el **Ejecutivo Comercial** (Tiempo Completo), como se muestra en el gráfico de **Productividad Media**. Sin embargo, su relación **costo/productividad** es más alta, lo que lo hace menos eficiente en términos de **costo** en comparación con otros cargos.
2. **El mejor costo promedio** lo tiene el **Ejecutivo Comercial Fines de Semana**, ya que este cargo tiene un costo más bajo en relación con las otras modalidades.
3. **La mejor relación Costo/Productividad** la tiene el **Ejecutivo Comercial Fines de Semana**, ya que tiene el valor **más bajo** de todos los cargos, lo que significa que este cargo es más eficiente en términos de **costo** por unidad de productividad.

#### Conclusiones:
- **El cargo más eficiente en términos de costo por productividad** es el **Ejecutivo Comercial Fines de Semana**, ya que tiene un **costo bajo** en comparación con la **productividad generada**.
- **Ejecutivo Comercial (Tiempo Completo)** tiene una **alta productividad** pero una **relación costo/productividad** más alta, lo que lo hace menos eficiente en términos de costo comparado con el cargo de **fines de semana**.

### **Estrategia Recomendada**:
- Para **incrementar la productividad**, la mejor opción es contratar **Ejecutivos Comerciales Fines de Semana**, ya que este cargo es el **más eficiente** al generar una mayor productividad por unidad de costo.


## Fase 3: Clasificación de los Puntos de Venta en Segmentos

### Descripción:
En esta fase, se aplicaron técnicas de **aprendizaje no supervisado** utilizando el dataset **"Segmentacion_CATT.xlsx"** para clasificar los puntos de venta en segmentos basados en patrones y características comunes.

#### Técnicas Empleadas:
- **K-means clustering**: Para la segmentación de los puntos de venta, utilizando **características numéricas** como **capturas de tarjetas**, **aprobación de créditos** y **monto de créditos**.
- **Método del Codo**: Para determinar el número óptimo de clusters, basado en la **inercia** de los modelos.
- **PCA (Análisis de Componentes Principales)**: Para reducir la dimensionalidad de los datos y visualizar los segmentos en un espacio 2D.

#### Resultados:
- Se identificaron **4 segmentos** distintos de puntos de venta:
  - **Segmento 0**: Puntos de venta con alto rendimiento en términos de capturas de tarjetas y aprobación de créditos.
  - **Segmento 1**: Puntos de venta con baja actividad comercial y falta de capturas de créditos.
  - **Segmento 2**: Puntos de venta con un buen aprovechamiento del tráfico, pero bajo volumen de créditos aprobados.
  - **Segmento 3**: Puntos de venta con alto tráfico pero bajo aprovechamiento del mismo.

#### Gráficos:
Se generaron tres **gráficos de barras** adicionales para comparar los siguientes totales por segmento:
1. **Total de Capturas de Tarjetas por Segmento**
2. **Total de Capturas de Créditos por Segmento**
3. **Total de Aprobación de Tarjetas por Segmento**

En todos estos gráficos, el **Segmento 0** mostró el **mejor desempeño** en cuanto a **capturas** y **aprobaciones**.

#### Estrategias Recomendadas:
1. **Para el Segmento 0 (alto rendimiento)**:
   - **Estrategias de Expansión**: Ampliar la **oferta de productos financieros**, como **préstamos personales** o **seguros**.
   - **Fidelización y recompensas**: Implementar programas de **fidelización** para asegurar la **retención de clientes**.
   - **Promociones de créditos**: Aumentar las **promociones** para **credibilidad de tarjetas y créditos**.

2. **Para los Segmentos 1 y 3 (bajo rendimiento)**:
   - **Segmento 1**: **Revisión de estrategias de captación de clientes**. Aumentar el **tráfico de clientes** y mejorar las **estrategias de marketing**.
   - **Segmento 3**: Mejorar el **aprovechamiento del tráfico** mediante **ofertas de crédito más atractivas**.

3. **Para el Segmento 2 (optimización)**:
   - **Optimizar la conversión de clientes**. Mejorar las conversiones a **créditos** mediante **estrategias de marketing** dirigidas a clientes específicos.

4. **Estrategias de colaboración**:
   - **Alianzas estratégicas** con **bancos o instituciones financieras** para ofrecer mejores productos de crédito.
   - **Capacitación de personal** para **mejorar el aprovechamiento del tráfico**.

## Fase 4: Presentación de Resultados

### Segmentación y Patrones Clave en los Puntos de Venta

1. **Segmento 0**: **Alto rendimiento en capturas y aprobaciones**
   - **Patrón**: Este segmento tiene un **alto volumen** en **capturas de tarjetas** y **aprobaciones de créditos**.
   
2. **Segmento 1**: **Bajo rendimiento en capturas y aprobaciones**
   - **Patrón**: Este segmento muestra **bajos niveles** de actividad en **capturas de tarjetas** y **aprobación de créditos**.

3. **Segmento 2**: **Optimización del rendimiento con bajo volumen**
   - **Patrón**: Aunque el segmento muestra un **alto aprovechamiento del tráfico**, el **volumen de aprobaciones de créditos** es bajo.

4. **Segmento 3**: **Alto tráfico pero bajo aprovechamiento**
   - **Patrón**: Este segmento tiene **alto volumen de tráfico**, pero **bajo aprovechamiento** en términos de créditos.

### Análisis de las Variables Relevantes

- **Segmento 0**: Contratar **Ejecutivos Comerciales a Tiempo Completo** para maximizar **captación de tarjetas y créditos** en puntos de venta con alto rendimiento.
- **Segmento 1**: Contratar **Ejecutivos Comerciales de Medio Tiempo** para aumentar **tráfico** y mejorar **conversiones a créditos** en puntos de venta con bajo rendimiento.
- **Segmento 2**: Contratar **Ejecutivos Comerciales de Medio Tiempo** para optimizar **conversiones a créditos** en puntos de venta con buen aprovechamiento de tráfico.
- **Segmento 3**: Contratar **Ejecutivos Comerciales de Medio Tiempo** para mejorar el **aprovechamiento del tráfico** y la conversión en puntos de venta con alto tráfico.

### Recomendaciones Estratégicas

1. **Segmento 0**: Contratar **Ejecutivos Comerciales (Tiempo Completo)** para maximizar las **aprobaciones de créditos** y **captación de tarjetas**.
2. **Segmento 1**: Contratar **Ejecutivos Comerciales de Medio Tiempo** para incrementar el tráfico y las conversiones a créditos.
3. **Segmento 2**: Contratar **Ejecutivos Comerciales de Medio Tiempo** con **foco en la conversión de clientes a créditos**.
4. **Segmento 3**: Contratar **Ejecutivos Comerciales de Medio Tiempo** para maximizar las conversiones a créditos durante los momentos de alto tráfico.

