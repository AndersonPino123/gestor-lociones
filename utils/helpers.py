# utils/helpers.py

import psycopg2
import streamlit as st

# Función para conectar a la base de datos

def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

# Función para obtener productos disponibles (para combos, compras, etc.)
def obtener_productos_disponibles():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, genero
        FROM productos
        WHERE disponible = true
        ORDER BY nombre_producto
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos