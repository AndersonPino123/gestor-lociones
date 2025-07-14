# modules/productos.py

import psycopg2
from database.connection import conectar

# ✅ Obtener todos los productos (para vista de administrador)
def obtener_todos_los_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, ref_proveedor, genero, fragancia,
               cantidad_ml, precio, stock, disponible, fecha_creacion, imagen_url
        FROM productos ORDER BY id
    """)
    datos = cursor.fetchall()
    conexion.close()
    columnas = ["ID", "Marca", "Nombre", "Referencia proveedor", "Género", "Fragancia",
                "Cantidad (ml)", "Precio", "Stock", "Disponible", "Fecha", "Imagen"]
    return datos, columnas

# ✅ Agregar nuevo producto (loción)
def agregar_locion(marca, nombre, ref_proveedor, genero, fragancia,
                   cantidad, precio, stock, disponible, imagen_url):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (
                marca, nombre_producto, ref_proveedor, genero, fragancia,
                cantidad_ml, precio, stock, disponible, imagen_url, fecha_creacion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
        """, (marca, nombre, ref_proveedor, genero, fragancia,
              cantidad, precio, stock, disponible, imagen_url))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        return f"Error al guardar loción: {e}"

# ✅ Obtener productos disponibles para compras
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

# ✅ Catálogo filtrado para visitantes/clientes
def obtener_catalogo(filtro):
    conexion = conectar()
    cursor = conexion.cursor()
    if filtro == "Todos":
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url
            FROM productos WHERE disponible = true ORDER BY nombre_producto;
        """)
    else:
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url
            FROM productos WHERE disponible = true AND genero = %s ORDER BY nombre_producto;
        """, (filtro.lower(),))
    productos = cursor.fetchall()
    conexion.close()
    return productos