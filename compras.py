from db import conectar
from datetime import date
from clientes import ver_clientes  # Para mostrar los clientes antes de comprar

conexion = conectar()
cursor = conexion.cursor()

# CREATE - Agregar compra
def agregar_compra():
    try:
        print("\n📋 Clientes disponibles:")
        ver_clientes()

        cliente_id = input("🆔 ID del cliente que hace la compra: ").strip()
        producto = input("🧴 Nombre del producto: ").strip()
        valor_input = input("💰 Valor del producto (sin puntos): ").strip()

        # Validaciones básicas
        if not cliente_id or not producto or not valor_input:
            print("⚠️ Todos los campos son obligatorios.")
            return

        if not cliente_id.isdigit():
            print("⚠️ El ID del cliente debe ser numérico.")
            return

        # Verificar si el cliente existe y está activo
        cursor.execute("SELECT id, activo FROM clientes WHERE id = %s", (cliente_id,))
        cliente = cursor.fetchone()

        if cliente is None:
            print("❌ El cliente no existe.")
            return
        if cliente[1] == False:
            print("⚠️ Este cliente está desactivado y no puede hacer compras.")
            return

        # Validar el valor
        try:
            valor = float(valor_input)
        except ValueError:
            print("⚠️ El valor debe ser un número.")
            return

        # Insertar compra
        cursor.execute("""
        INSERT INTO compras (cliente_id, producto, valor, fecha)
        VALUES (%s, %s, %s, %s)
        """, (cliente_id, producto, valor, date.today()))
        conexion.commit()
        print("✅ Compra registrada con éxito.")

    except Exception as e:
        print("❌ Error al registrar la compra.")
        print("💥 Detalles:", e)
        
# UPDATE - Editar compra
def editar_compra():
    try:
        ver_compras()
        id_compra = input("🆔 ID de la compra a editar: ").strip()

        if not id_compra.isdigit():
            print("⚠️ El ID debe ser un número.")
            return

        # Verificamos si la compra existe
        cursor.execute("SELECT * FROM compras WHERE id = %s", (id_compra,))
        compra_existente = cursor.fetchone()
        if compra_existente is None:
            print("❌ La compra no existe.")
            return

        nuevo_producto = input("🧴 Nuevo nombre del producto: ").strip()
        nuevo_valor_input = input("💰 Nuevo valor: ").strip()

        if not nuevo_producto or not nuevo_valor_input:
            print("⚠️ Todos los campos son obligatorios.")
            return

        try:
            nuevo_valor = float(nuevo_valor_input)
            if nuevo_valor <= 0:
                print("⚠️ El valor debe ser mayor a 0.")
                return
        except ValueError:
            print("⚠️ El valor debe ser numérico.")
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
        id_compra = input("🆔 ID de la compra a eliminar: ").strip()

        if not id_compra.isdigit():
            print("⚠️ El ID debe ser un número.")
            return

        # Verificamos si existe la compra
        cursor.execute("SELECT * FROM compras WHERE id = %s", (id_compra,))
        compra = cursor.fetchone()
        if compra is None:
            print("❌ La compra no existe.")
            return

        confirmacion = input("❓ ¿Seguro que deseas eliminar esta compra? (s/n): ").lower()
        if confirmacion == "s":
            cursor.execute("DELETE FROM compras WHERE id = %s", (id_compra,))
            conexion.commit()
            print("🗑️ Compra eliminada.")
        else:
            print("❌ Eliminación cancelada.")

    except Exception as e:
        print("❌ Error al eliminar la compra.")
        print("💥 Detalles:", e)