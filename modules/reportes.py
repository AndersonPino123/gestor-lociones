import pandas as pd
from database.connection import obtener_conexion_cursor

def resumen_ventas_mes():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("""
        SELECT SUM(valor) FROM compras
        WHERE DATE_PART('month', fecha) = DATE_PART('month', CURRENT_DATE)
        AND DATE_PART('year', fecha) = DATE_PART('year', CURRENT_DATE);
    """)
    total = cursor.fetchone()[0] or 0
    conexion.close()
    return total

def compras_por_cliente():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("""
        SELECT c.nombre, COUNT(co.id) AS cantidad, SUM(co.valor) AS total
        FROM clientes c
        JOIN compras co ON c.id = co.cliente_id
        GROUP BY c.nombre
        ORDER BY total DESC;
    """)
    resultados = cursor.fetchall()
    conexion.close()
    return pd.DataFrame(resultados, columns=["Cliente", "Compras", "Total gastado"])