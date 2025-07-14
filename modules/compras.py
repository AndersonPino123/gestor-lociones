from database.connection import conectar

def obtener_clientes_activos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE activo = true ORDER BY nombre")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def registrar_compra(cliente_id, producto, valor):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO compras (cliente_id, producto, valor, fecha)
        VALUES (%s, %s, %s, CURRENT_DATE)
    """, (cliente_id, producto, valor))
    conexion.commit()
    conexion.close()