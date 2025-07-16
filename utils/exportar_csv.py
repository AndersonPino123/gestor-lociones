import os
import csv
from gestor_lociones.database.db import conectar

conexion = conectar()
cursor = conexion.cursor()

def exportar_compras_con_clientes():
    try:
        cursor.execute("""
            SELECT c.nombre, co.producto, co.valor, co.fecha
            FROM clientes c
            INNER JOIN compras co ON c.id = co.cliente_id
            ORDER BY co.fecha;
        """)
        resultados = cursor.fetchall()

        with open("reporte_compras.csv", mode="w", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Cliente", "Producto", "Valor", "Fecha"])
            for fila in resultados:
                escritor.writerow(fila)

        print("✅ Reporte exportado correctamente como reporte_compras.csv")
        os.system("open reporte_compras.csv")  # ✅ Aquí sí es correcto abrirlo

    except Exception as e:
        print("❌ Error al exportar el reporte.")
        print("💥 Detalles:", e)