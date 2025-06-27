from db import conectar
from datetime import date
from clientes import ver_clientes  # Para mostrar los clientes antes de comprar

conexion = conectar()
cursor = conexion.cursor()

# CREATE - Agregar compra
def agregar_compra():
    try:
        print("\n📋 Clientes disponibles:")
        ver_clientes()  # Mostrar los clientes existentes antes de pedir ID

        cliente_id = input("ID del cliente que hace la compra: ").strip()
        producto = input("Nombre del producto: ").strip()
        valor = input("Valor del producto (sin puntos): ").strip()

        # Validaciones
        if not cliente_id or not producto or not valor:
            print("⚠️ Todos los campos son obligatorios.")
            return

        if not cliente_id.isdigit():
            print("⚠️ El ID del cliente debe ser un número.")
            return

        try:
            valor = float(valor)
        except ValueError:
            print("⚠️ El valor debe ser un número.")
            return

        # Inserción en la base de datos
        cursor.execute("""
        INSERT INTO compras (cliente_id, producto, valor, fecha)
        VALUES (%s, %s, %s, %s)
        """, (cliente_id, producto, valor, date.today()))
        conexion.commit()
        print("✅ Compra registrada con éxito.")
    
    except Exception as e:
        print("❌ Error al registrar la compra.")
        print("💥 Detalles:", e)
        
# READ - Ver compras
def ver_compras():
   try: 
    cursor.execute("SELECT * FROM compras ORDER BY id")
    resultados = cursor.fetchall()
    print("\n🛒 Lista de compras:")
    for fila in resultados:
        print(f"ID: {fila[0]} | Producto: {fila[1]} | Valor: ${fila[2]} | Fecha: {fila[3]} | Cliente ID: {fila[4]}")
   except Exception as e:
       print("❌ Error al ver la compra.")
       print("💥 Detalles:", e)

# UPDATE - Editar compra
def editar_compra():
    try:
        ver_compras()
        id_compra = input("ID de la compra a editar: ").strip()
        
        if not id_compra.isdigit():
            print("⚠️ El ID debe ser un número.")
            return

        nuevo_producto = input("Nuevo nombre del producto: ").strip()
        nuevo_valor = input("Nuevo valor: ").strip()

        if not nuevo_producto or not nuevo_valor:
            print("⚠️ Todos los campos son obligatorios.")
            return

        try:
            nuevo_valor = float(nuevo_valor)
        except ValueError:
            print("⚠️ El valor debe ser un número.")
            return

        cursor.execute("""
        UPDATE compras
        SET producto = %s, valor = %s
        WHERE id = %s
        """, (nuevo_producto, nuevo_valor, id_compra))
        conexion.commit()
        print("✏️ Compra actualizada.")
    
    except Exception as e:
        print("❌ Error al editar la compra.")
        print("💥 Detalles:", e)

# DELETE - Eliminar compra
def eliminar_compra():
   try: 
    ver_compras()
    id_compra = input("ID de la compra a eliminar: ").strip()
    
    if not id_compra.isdigit():
        print("⚠️ El id debe ser un número.")
        return
    
    confirmacion = input("¿Seguro que deseas eliminar esta compra? (s/n): ").lower()
    if confirmacion.lower() == "s":
        cursor.execute("DELETE FROM compras WHERE id = %s", (id_compra,))
        conexion.commit()
        print("🗑️ Compra eliminada.")
    else:
        print("❌ Acción cancelada.")
   except Exception as e:
       print("❌ Error al eliminar el cliente.")     
       print("💥 Detalles:", e)

