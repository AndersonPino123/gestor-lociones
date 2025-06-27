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
    nombre = input("Nombre: ").stripe() #.stripe elimina espacios vacíos y saltos de linea \n
    correo = input("Correo: ").stripe()
    edad = input("Edad: ").stripe()
    
    #validación
    if not nombre or not correo or not edad: #if not asegura que no este vacio
      print("⚠️ Todos los campos son obligatorios.")
      return
    
    if "@" not in correo: # "@" not in correo hace una validación ráida de email
      print("⚠️ Correo no valido (falta '@').")
      return
    
    if not edad.isdigit(): #.isdigit() verifica que edad sea un número
      print("⚠️ La edad debe ser un número.")
      return
    
    edad = int(edad)
    activo = True

    cursor.execute("""
    INSERT INTO clientes (nombre, correo, edad, activo)
    VALUES (%s, %s, %s, %s)
    """, (nombre, correo, edad, activo))
    conexion.commit()
    print("✅ Cliente agregado con éxito.")
 except Exception as e:
     print("❌ Error al agregar cliente.")
     print("💥 Detalles:", e)

     
def editar_cliente():
  try:
    ver_clientes()
    id_cliente = input("ID del cliente a editar: ").stripe()
    
    if not id_cliente.isdigit():
      print("⚠️ Debe ingresar un número de ID válido.")
      return
    
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_correo = input("Nuevo correo: ").strip()
    nueva_edad = input("Nueva edad: ").strip()

    #validación
    if not nuevo_nombre or not nuevo_correo or not nueva_edad:
      print(" Todos los campos deben ser obligatorios.")
      return
    
    if "@" not in nuevo_correo:
      print("⚠️ Correo no valido.")
      return
    
    if not nueva_edad.isdigit():
      print("⚠️ La edad debe ser un número.")
      return
    
    cursor.execute("""
    UPDATE clientes
    SET nombre = %s, correo = %s, edad = %s
    WHERE id = %s
    """, (nuevo_nombre, nuevo_correo, nueva_edad, id_cliente))
    conexion.commit()
    print("✏️ Cliente actualizado.")
  except Exception as e:
     print("❌ Error al editar el cliente")
     print("💥 Detalles:", e)

#Tambíen la mejoramos para evitar errores si ingresan letras en lugar de numeros

def eliminar_cliente():
  try:
    ver_clientes()
    id_cliente = input("ID del cliente a eliminar: ").strip()
    
    #validación
    if not id_cliente.isdigit():
      print("⚠️ El ID debe ser un número valido.")
      return
    
    confirmacion = input("¿Estás seguro de eliminar este cliente? (s/n): ").lower()
    if confirmacion.lower() == "s":
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
        conexion.commit()
        print("🗑️ Cliente eliminado.")
    else:
        print("❌ Eliminación cancelada.")
  except Exception as e:
      print("❌ Error al eliminar el cliente.")     
      print("💥 Detalles: ", e)

#Agregamos control en la desactivación

def desactivar_cliente():
   try: 
    ver_clientes()
    id_cliente = input("ID del cliente a desactivar: ").strip()
    
    #validación
    if not id_cliente.isdigit():
      print("⚠️ ID no valido.")
      return
      
    confirmacion = input("¿Estás seguro de desactivarlo? (s/n): ")
    if confirmacion.lower() == "s":
        cursor.execute("UPDATE clientes SET activo = FALSE WHERE id = %s", (id_cliente,))
        conexion.commit()
        print("🚫 Cliente desactivado.")
    else:
        print("❌ Acción cancelada.")
   except Exception as e:
    print("❌ Error al desactivar el cliente.")
    print("💥 Detalles: ",e)