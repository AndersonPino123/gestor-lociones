from db import conectar
conexion = conectar()
cursor = conexion.cursor()

def reporte_compras_con_clientes():
    cursor.execute("""
    SELECT c.nombre, co.producto, co.valor, co.fecha
    FROM clientes c
    INNER JOIN compras co ON c.id = co.cliente_id
    ORDER BY co.id;
    """)
    resultados = cursor.fetchall()

    print("\n🧾 Reporte de compras:")
    for fila in resultados:
        print(f"Cliente: {fila[0]} | Producto: {fila[1]} | Valor: ${fila[2]} | Fecha: {fila[3]}")
        
#Muestra todas las compras hechas por un cliente especifico:
def compras_por_cliente():
    try:
        id_cliente = input("🆔 Ingresa el ID del cliente: ")

        cursor.execute("""
        SELECT c.nombre, co.producto, co.valor, co.fecha
        FROM clientes c
        INNER JOIN compras co ON c.id = co.cliente_id
        WHERE c.id = %s
        ORDER BY co.fecha;
        """, (id_cliente,))

        resultados = cursor.fetchall()

        if resultados:
            print(f"\n🧾 Compras realizadas por {resultados[0][0]}:")
            for fila in resultados:
                print(f"- Producto: {fila[1]} | Valor: ${fila[2]} | Fecha: {fila[3]}")
        else:
            print("⚠️ Este cliente no tiene compras registradas.")

    except Exception as e:
        print("❌ Error al generar el reporte.")
        print("💥 Detalles:", e)

# Muestra el total gastado y el total de compras
def resumen_compras_cliente():
    try:
        id_cliente = input("🆔 Ingresa el ID del cliente: ")

        cursor.execute("""
        SELECT c.nombre, COUNT(co.id) AS cantidad, SUM(co.valor) AS total
        FROM clientes c
        INNER JOIN compras co ON c.id = co.cliente_id
        WHERE c.id = %s
        GROUP BY c.nombre;
        """, (id_cliente,))

        resultado = cursor.fetchone()

        if resultado:
            print(f"\n📊 Resumen de {resultado[0]}:")
            print(f"🛒 Compras realizadas: {resultado[1]}")
            print(f"💰 Total gastado: ${resultado[2]}")
        else:
            print("⚠️ Este cliente no tiene compras registradas.")

    except Exception as e:
        print("❌ Error al generar el resumen.")
        print("💥 Detalles:", e)
        
# Reporte general: todos los clientes con total de compras

def resumen_general_compras():
    try:
        cursor.execute("""
        SELECT c.nombre, COUNT(co.id) AS compras, COALESCE(SUM(co.valor), 0) AS total
        FROM clientes c
        LEFT JOIN compras co ON c.id = co.cliente_id
        GROUP BY c.nombre
        ORDER BY total DESC;
        """)

        resultados = cursor.fetchall()

        print("\n📊 Resumen general de compras:")
        for fila in resultados:
            print(f"🧑 {fila[0]} | 🛒 Compras: {fila[1]} | 💰 Total gastado: ${fila[2]}")
    except Exception as e:
        print("❌ Error al generar el resumen general.")
        print("💥 Detalles:", e)