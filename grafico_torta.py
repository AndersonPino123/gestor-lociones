import psycopg2
import matplotlib.pyplot as plt

# Conexión
conexion = psycopg2.connect(
    host="localhost",
    database="gestor_contactos",
    user="postgres",
    password="1030622188"
)

cursor = conexion.cursor()

# Consulta: gasto total por cliente
cursor.execute("""
    SELECT c.nombre, SUM(co.valor)
    FROM clientes c
    JOIN compras co ON c.id = co.cliente_id
    GROUP BY c.nombre
    ORDER BY SUM(co.valor) DESC;
""")

resultados = cursor.fetchall()
cursor.close()
conexion.close()

# Separar datos
nombres = [fila[0] for fila in resultados]
gastos = [fila[1] for fila in resultados]

# Gráfico de torta
plt.figure(figsize=(8, 6))
plt.pie(gastos, labels=nombres, autopct='%1.1f%%', startangle=140)
plt.title("🍰 Porcentaje de gasto por cliente")
plt.axis("equal")  # Hace que el círculo no se vea ovalado
plt.tight_layout()
plt.show()