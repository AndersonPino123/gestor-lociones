# archivo modules/clientes.py
from database.connection import conectar

def ver_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, edad, activo, creado_en FROM clientes ORDER BY id")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def actualizar_cliente(id_cliente, nuevo_nombre, nuevo_correo, nueva_edad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE clientes SET nombre=%s, correo=%s, edad=%s
        WHERE id=%s
    """, (nuevo_nombre, nuevo_correo, nueva_edad, id_cliente))
    conexion.commit()
    conexion.close()

def cambiar_estado_cliente(id_cliente, nuevo_estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE clientes SET activo=%s WHERE id=%s", (nuevo_estado, id_cliente))
    conexion.commit()
    conexion.close()
    
def agregar_cliente(nombre, correo, edad):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO clientes (nombre, correo, edad)
            VALUES (%s, %s, %s)
        """, (nombre, correo, edad))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("❌ Error al agregar cliente:", e)
        return False

def obtener_clientes_activos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE activo = true ORDER BY nombre")
    datos = cursor.fetchall()
    conexion.close()
    return datos