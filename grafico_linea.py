import psycopg2
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# Conexión
conexion = psycopg2.connect(
    host="localhost",
    database="gestor_contactos",
    user="postgres",
    password="1030622188"
)

cursor = conexion.cursor()

# Consulta: total de compras por fecha
cursor.execute("""
    SELECT fecha, SUM(valor)
    FROM compras
    GROUP BY fecha
    ORDER BY fecha;
""")

resultados = cursor.fetchall()
cursor.close()
conexion.close()

# Separar fechas y totales
fechas = [fila[0] for fila in resultados]
totales = [fila[1] for fila in resultados]

# Convertir fechas a texto si es necesario
fechas_str = [fecha.strftime('%Y-%m-%d') for fecha in fechas]

# Crear gráfica de línea
plt.figure(figsize=(10, 6))
plt.plot(fechas_str, totales, marker='o', linestyle='-', color='blue')
plt.title("📈 Evolución de compras por fecha")
plt.xlabel("Fecha")
plt.ylabel("Total gastado")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()