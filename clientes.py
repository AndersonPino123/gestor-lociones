from db import conectar
conexion = conectar()
cursor = conexion.cursor()

def ver_clientes():
   try: 
    cursor.execute("SELECT * FROM clientes ORDER BY id")
    resultados = cursor.fetchall()
    print("\n📋 Lista de clientes:")
    for fila in resultados:
        estado = "✅ Activo" if fila[4] else "❌ Inactivo"
        print(f"ID: {fila[0]} | Nombre: {fila[1]} | Correo: {fila[2]} | Edad: {fila[3]} | Estado: {estado} | Fecha: {fila[5]}")
   except Exception as e:
       print("❌ Error al ver el cliente.")
       print("💥 Detalles: ", e)
       
def agregar_cliente():
    try:
        nombre = input("Nombre: ").strip()
        correo = input("Correo: ").strip()
        edad = input("Edad: ").strip()

        # Validaciones:
        if len(nombre) < 3 or not nombre.replace(" ", "").isalpha():
            print("⚠️ El nombre debe tener al menos 3 letras y no contener números.")
            return

        if "@" not in correo or "." not in correo:
            print("⚠️ El correo no parece válido (falta @ o .)")
            return

        if not edad.isdigit() or not (0 < int(edad) <= 120):
            print("⚠️ La edad debe ser un número entre 1 y 120.")
            return

        # Insertar si todo está bien
        cursor.execute("""
            INSERT INTO clientes (nombre, correo, edad)
            VALUES (%s, %s, %s)
        """, (nombre, correo, int(edad)))
        conexion.commit()
        print("✅ Cliente agregado con éxito.")
    
    except Exception as e:
        print("❌ Error al agregar cliente.")
        print("💥 Detalles:", e)
     
def editar_cliente():
    ver_clientes()
    id_cliente = input("🆔 ID del cliente a editar: ").strip()

    if not id_cliente.isdigit() or int(id_cliente) <= 0:
        print("⚠️ Debes ingresar un ID válido.")
        return

    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_correo = input("Nuevo correo: ").strip()
    nueva_edad = input("Nueva edad: ").strip()

    if len(nuevo_nombre) < 3:
        print("⚠️ El nombre debe tener al menos 3 letras.")
        return

    if "@" not in nuevo_correo or "." not in nuevo_correo:
        print("⚠️ El correo debe ser válido (ej: ejemplo@correo.com).")
        return

    if not nueva_edad.isdigit() or int(nueva_edad) <= 0:
        print("⚠️ La edad debe ser un número positivo.")
        return

    try:
        cursor.execute("""
            UPDATE clientes
            SET nombre = %s, correo = %s, edad = %s
            WHERE id = %s
        """, (nuevo_nombre, nuevo_correo, nueva_edad, id_cliente))
        conexion.commit()
        print("✅ Cliente actualizado con éxito.")
    except Exception as e:
        print("❌ Error al actualizar el cliente.")
        print("💥 Detalles:", e)
        
#Tambíen la mejoramos para evitar errores si ingresan letras en lugar de numeros

def eliminar_cliente():
    ver_clientes()
    id_cliente = input("🆔 ID del cliente a eliminar: ").strip()

    if not id_cliente.isdigit() or int(id_cliente) <= 0:
        print("⚠️ Debes ingresar un ID válido.")
        return

    # Verificamos si el cliente existe
    cursor.execute("SELECT id FROM clientes WHERE id = %s", (id_cliente,))
    if cursor.fetchone() is None:
        print("⚠️ El cliente no existe.")
        return

    confirmacion = input("¿Estás seguro de eliminar este cliente? (s/n): ").lower()
    if confirmacion == "s":
        try:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            conexion.commit()
            print("🗑️ Cliente eliminado.")
        except Exception as e:
            print("❌ Error al eliminar cliente.")
            print("💥 Detalles:", e)
    else:
        print("❌ Eliminación cancelada.")
#Agregamos control en la desactivación

def desactivar_cliente():
    ver_clientes()
    id_cliente = input("🆔 ID del cliente a desactivar: ").strip()

    if not id_cliente.isdigit() or int(id_cliente) <= 0:
        print("⚠️ El ID debe ser un número válido.")
        return

    # Validamos si el cliente existe
    cursor.execute("SELECT id, activo FROM clientes WHERE id = %s", (id_cliente,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("❌ El cliente no existe.")
        return

    if resultado[1] == False:
        print("⚠️ Este cliente ya está desactivado.")
        return

    confirmacion = input("¿Deseas desactivar este cliente? (s/n): ").lower()
    if confirmacion == "s":
        try:
            cursor.execute("UPDATE clientes SET activo = FALSE WHERE id = %s", (id_cliente,))
            conexion.commit()
            print("🔒 Cliente desactivado exitosamente.")
        except Exception as e:
            print("❌ Error al desactivar cliente.")
            print("💥 Detalles:", e)
    else:
        print("❌ Acción cancelada.")
        
def reactivar_cliente():
    ver_clientes()
    id_cliente = input("🆔 ID del cliente a reactivar: ").strip()

    if not id_cliente.isdigit() or int(id_cliente) <= 0:
        print("⚠️ El ID debe ser un número válido.")
        return

    # Validamos si el cliente existe
    cursor.execute("SELECT id, activo FROM clientes WHERE id = %s", (id_cliente,))
    resultado = cursor.fetchone()

    if resultado is None:
        print("❌ El cliente no existe.")
        return

    if resultado[1] == True:
        print("⚠️ Este cliente ya está activo.")
        return

    confirmacion = input("¿Deseas reactivar este cliente? (s/n): ").lower()
    if confirmacion == "s":
        try:
            cursor.execute("UPDATE clientes SET activo = TRUE WHERE id = %s", (id_cliente,))
            conexion.commit()
            print("✅ Cliente reactivado exitosamente.")
        except Exception as e:
            print("❌ Error al reactivar cliente.")
            print("💥 Detalles:", e)
    else:
        print("❌ Acción cancelada.")