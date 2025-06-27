import psycopg2
import matplotlib.pyplot as plt

# Conexión a la base de datos
conexion = psycopg2.connect(
    host="localhost",
    database="gestor_contactos",
    user="postgres",
    password="1030622188"
)

cursor = conexion.cursor()

# Consulta: total de compras por cliente
cursor.execute("""
    SELECT c.nombre, COUNT(co.id) 
    FROM clientes c
    JOIN compras co ON c.id = co.cliente_id
    GROUP BY c.nombre
    ORDER BY COUNT(co.id) DESC
""")

resultados = cursor.fetchall()
cursor.close()
conexion.close()

# Separar nombres y cantidades
nombres = [fila[0] for fila in resultados]
compras = [fila[1] for fila in resultados]

# Crear gráfica de barras
plt.bar(nombres, compras, color='skyblue')
plt.title("Total de compras por cliente")
plt.xlabel("Cliente")
plt.ylabel("Cantidad de compras")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()