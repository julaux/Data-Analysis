# Proyecto ETL - Prueba Técnica R1

Este proyecto implementa un proceso **ETL (Extracción, Transformación y Carga)** que se conecta a una base de datos SQLite, extrae datos de archivos CSV, los transforma (eliminando tildes y comas) y los carga en la base de datos.

## Descripción

Este script realiza las siguientes operaciones:

1. **Extracción**: Los datos se extraen desde cuatro archivos CSV ubicados en la carpeta `Tablas/`.
2. **Transformación**: Se realiza una limpieza de datos.
3. **Carga**: Se cargan los datos en las tablas correspondientes, la base de datos es `Python_test.db`.

## Estructura del Proyecto
Proyecto_ETL/
├── Tablas/
│ ├── estudiantes.csv
│ ├── asignaturas.csv
│ ├── profesores.csv
│ └── historial_academico.csv
└── ETL.py

- **Tablas/**: Contiene los archivos CSV con los datos de entrada.
  - `estudiantes.csv`: Datos de los estudiantes.
  - `asignaturas.csv`: Información sobre las asignaturas.
  - `profesores.csv`: Información sobre los profesores.
  - `historial_academico.csv`: Relaciona a los estudiantes con sus asignaturas, profesores y calificaciones.
- **ETL.py**: El script Python que realiza el proceso ETL.
