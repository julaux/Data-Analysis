"""
Este script es un ETL que realiza conexión a una base de datos, extrae los datos, los transforma,  elimina y carga los datos.
"""
import sqlite3
import os
import pandas as pd
import unicodedata

# DIRECTORIO ACTUAL
cwd = os.getcwd()


# ---------- PASO 2.1 CONEXIÓN A LA ASE DE DATOS DESDE PYTHON ----------

# FUNCIÓN CONEXIÓN A LA BASE DE DATOS
def conectar_db():
    """
    Conecta con la base de datos
    """
    # PATH DE LA BASE DE DATOS
    db_path = os.path.join(cwd, 'Python_test.db')

    # CONEXIÓN A LA BASE DE DATOS   
    conn = sqlite3.connect(db_path)

    return conn


# ---------- PASO 2.2 EXTRACCIÓN DE DATOS ----------

# EXTRACCIÓN DE DATOS
def extraer_datos():
    """
    Extrae los datos de la base de datos
    """
    cwd = os.getcwd()

    # RUTA DE LOS ARCHIVOS CSV EN LA CARPETA 'Tablas'
    archivo_estudiantes = os.path.join(cwd, 'Tablas/estudiantes.csv')
    archivo_asignaturas = os.path.join(cwd, 'Tablas/asignaturas.csv')
    archivo_profesores = os.path.join(cwd, 'Tablas/profesores.csv')
    archivo_historial = os.path.join(cwd, 'Tablas/historial_academico.csv')

    # CARGA DE DATOS EN DATAFRAMES
    df_estudiantes = pd.read_csv(archivo_estudiantes, sep=',', encoding='utf-8')
    df_asignaturas = pd.read_csv(archivo_asignaturas, sep=',', encoding='utf-8')
    df_profesores = pd.read_csv(archivo_profesores, sep=',', encoding='utf-8')
    df_historial = pd.read_csv(archivo_historial, sep=',', encoding='utf-8')

    return df_estudiantes, df_asignaturas, df_profesores, df_historial


# ---------- PASO 2.3 TRANSFORMACIÓN DE DATOS ----------

# LIMPIEZA DE DATOS
def limpiar_texto(texto):
    """
    Función para limpiar texto: quitar tildes y comas.
    """
    # REMOVER TILDES Y CARACTERES ESPECIALES
    texto = unicodedata.normalize('NFD', texto)  
    texto = ''.join([c for c in texto if unicodedata.category(c) != 'Mn'])  # ELIMINA CARACTERES COMO DE CATEGORIA 'Mn'(tildes, etc.)
    
    # REMOVER COMAS
    texto = texto.replace(',', '')  

    return texto

def transformar_datos(df_estudiantes, df_asignaturas, df_profesores, df_historial):
    """
    Transforma los datos de los DataFrames

    Args:
        df_estudiantes (DataFrame): DataFrame de estudiantes.
        df_asignaturas (DataFrame): DataFrame de asignaturas.
        df_profesores (DataFrame): DataFrame de profesores.
        df_historial (DataFrame): DataFrame de historial académico.
    """

    # LIMPIEZA DE DATOS
    df_estudiantes['nombre_estudiante'] = df_estudiantes['nombre_estudiante'].apply(limpiar_texto)
    df_asignaturas['nombre_asignatura'] = df_asignaturas['nombre_asignatura'].apply(limpiar_texto)
    df_profesores['nombre_profesor'] = df_profesores['nombre_profesor'].apply(limpiar_texto)
    df_profesores['departamento'] = df_profesores['departamento'].apply(limpiar_texto)

    # ELIMINAR FILAS CON DATOS FALTANTES
    df_estudiantes['nombre_estudiante'] = df_estudiantes['nombre_estudiante'].dropna()

    # CORRECIÓN DATOS NUMERICOS
    df_historial['calificacion'] = df_historial['calificacion'].astype(float)

    return df_estudiantes, df_asignaturas, df_profesores, df_historial



# ---------- PASO 2.4 CARGA DE DATOS ----------

def cargar_datos(conn, df_estudiantes, df_asignaturas, df_profesores, df_historial):
    cursor = conn.cursor()

    # ELIMINAR DATOS DE LAS TABLAS
    cursor.execute('DELETE FROM historial_academico')
    cursor.execute('DELETE FROM estudiantes')
    cursor.execute('DELETE FROM asignaturas')
    cursor.execute('DELETE FROM profesores')

    # CARGAR DATOS TRANSFORMADOS EN LAS TABLAS
    for _, row in df_estudiantes.iterrows():
        cursor.execute('INSERT INTO estudiantes (nombre_estudiante) VALUES (?)', (row['nombre_estudiante'],))

    for _, row in df_asignaturas.iterrows():
        cursor.execute('INSERT INTO asignaturas (nombre_asignatura) VALUES (?)', (row['nombre_asignatura'],))

    for _, row in df_profesores.iterrows():
        cursor.execute('INSERT INTO profesores (nombre_profesor, departamento) VALUES (?, ?)', 
                       (row['nombre_profesor'], row['departamento']))

    for _, row in df_historial.iterrows():
        cursor.execute('INSERT INTO historial_academico (id_estudiante, id_asignatura, id_profesor, calificacion) VALUES (?, ?, ?, ?)', 
                       (row['id_estudiante'], row['id_asignatura'], row['id_profesor'], row['calificacion']))

    # GUARDAR CAMBIOS EN LA BASE DE DATOS
    conn.commit()


# ---------- FUNCIÓN DE EJECUCIÓN DEL ETL ----------

def ejecutar_etl():
    """
    Ejecuta el proceso ETL: conecta a la base de datos, extrae, transforma y carga los datos.
    """
    conn = conectar_db()
    
    # EXTRACCIÓN DE DATOS
    df_estudiantes, df_asignaturas, df_profesores, df_historial = extraer_datos()

    # TRANSFORMACIÓN DE LOS DATOS
    df_estudiantes, df_asignaturas, df_profesores, df_historial = transformar_datos(
        df_estudiantes, df_asignaturas, df_profesores, df_historial
    )

    # CARGA DE DATOS EN LA BASE DE DATOS
    cargar_datos(conn, df_estudiantes, df_asignaturas, df_profesores, df_historial)
    
    # CERRAR CONEXIÓN A LA BASE DE DATOS
    conn.close()

    print("ETL completado exitosamente.")

# EJECUTAR EL ETL
ejecutar_etl()

