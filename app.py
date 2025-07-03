import streamlit as st
import psycopg2
import pandas as pd

# Título
st.title("🧴 Gestor de Lociones - Streamlit")

# Conexión a PostgreSQL
def conectar():
    return psycopg2.connect(
        host="localhost",
        database="gestor_contactos",
        user="postgres",
        password="1030622188"  # <- puedes ocultarlo con st.secrets más adelante
    )

# Mostrar clientes
def ver_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, edad, activo, creado_en FROM clientes ORDER BY id")
    datos = cursor.fetchall()
    columnas = ["ID", "Nombre", "Correo", "Edad", "Activo", "Creado en"]
    df = pd.DataFrame(datos, columns=columnas)
    conexion.close()
    return df

# Mostrar productos (lociones)
def ver_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, fragancia, cantidad_ml, precio, disponible, fecha_creacion FROM productos ORDER BY id")
    datos = cursor.fetchall()
    columnas = ["ID", "Nombre", "Fragancia", "Cantidad (ml)", "Precio", "Disponible", "Fecha"]
    df = pd.DataFrame(datos, columns=columnas)
    conexion.close()
    return df

# Elegir qué ver
opcion = st.sidebar.selectbox("📂 Menú:", ["Clientes", "Lociones", "Agregar compra", "Ver compras"])

if opcion == "Clientes":
    st.subheader("👤 Lista de Clientes")
    
    df_clientes = ver_clientes()
    st.dataframe(df_clientes, use_container_width=True)

    # Editar o eliminar cliente
    st.markdown("### ✏️ Editar o 🗑️ Eliminar Cliente")
    id_editar = st.number_input("🔍 Ingresa el ID del cliente", min_value=1, step=1)

    accion = st.radio("Acción", ["Editar", "Eliminar"])

    if accion == "Editar":
        nombre_nuevo = st.text_input("Nuevo nombre")
        correo_nuevo = st.text_input("Nuevo correo")
        edad_nueva = st.number_input("Nueva edad", min_value=0, max_value=120, step=1)
        actualizar = st.button("💾 Actualizar")

        if actualizar:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE clientes SET nombre = %s, correo = %s, edad = %s
                    WHERE id = %s
                """, (nombre_nuevo.strip(), correo_nuevo.strip(), edad_nueva, id_editar))
                conexion.commit()
                conexion.close()
                st.success("✅ Cliente actualizado correctamente.")
            except Exception as e:
                st.error(f"❌ Error al actualizar: {e}")

    elif accion == "Eliminar":
        confirmar = st.checkbox("¿Estás seguro de eliminar este cliente?")
        if confirmar:
            eliminar = st.button("🗑️ Eliminar ahora")
            if eliminar:
                try:
                    conexion = conectar()
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id = %s", (id_editar,))
                    conexion.commit()
                    conexion.close()
                    st.success("✅ Cliente eliminado correctamente.")
                except Exception as e:
                    st.error(f"❌ Error al eliminar: {e}")

    # Agregar nuevo cliente
    st.markdown("---")
    st.subheader("➕ Agregar nuevo cliente")

    with st.form("form_cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        submit = st.form_submit_button("Guardar")

        if submit:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO clientes (nombre, correo, edad)
                    VALUES (%s, %s, %s)
                """, (nombre.strip(), correo.strip(), edad))
                conexion.commit()
                conexion.close()
                st.success("✅ Cliente agregado con éxito.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                
elif opcion == "Lociones":
    st.subheader("🧴 Lista de Lociones")
    df_productos = ver_productos()
    st.dataframe(df_productos, use_container_width=True)

    # Editar o eliminar loción
    st.markdown("### ✏️ Editar o 🗑️ Eliminar Loción")
    id_locion = st.number_input("🔍 Ingresa el ID de la loción", min_value=1, step=1)
    accion = st.radio("Acción", ["Editar", "Eliminar"], key="accion_locion")

    if accion == "Editar":
        nuevo_nombre = st.text_input("Nuevo nombre del producto")
        nueva_fragancia = st.text_input("Nueva fragancia")
        nueva_cantidad = st.number_input("Nueva cantidad (ml)", min_value=10, step=10)
        nuevo_precio = st.number_input("Nuevo precio", min_value=0.0, step=1000.0)
        disponible = st.checkbox("¿Disponible?", value=True, key="disponible_edit")
        actualizar = st.button("💾 Actualizar loción")

        if actualizar:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    UPDATE productos
                    SET nombre = %s, fragancia = %s, cantidad_ml = %s, precio = %s, disponible = %s
                    WHERE id = %s
                """, (nuevo_nombre.strip(), nueva_fragancia.strip(), nueva_cantidad, nuevo_precio, disponible, id_locion))
                conexion.commit()
                conexion.close()
                st.success("✅ Loción actualizada correctamente.")
            except Exception as e:
                st.error(f"❌ Error al actualizar: {e}")

    elif accion == "Eliminar":
        confirmar = st.checkbox("¿Estás seguro de eliminar esta loción?", key="confirmar_eliminar")
        if confirmar:
            eliminar = st.button("🗑️ Eliminar ahora")
            if eliminar:
                try:
                    conexion = conectar()
                    cursor = conexion.cursor()
                    cursor.execute("DELETE FROM productos WHERE id = %s", (id_locion,))
                    conexion.commit()
                    conexion.close()
                    st.success("✅ Loción eliminada correctamente.")
                except Exception as e:
                    st.error(f"❌ Error al eliminar: {e}")

    # Agregar nueva loción
    st.markdown("---")
    st.subheader("➕ Agregar nueva loción")

    with st.form("form_locion"):
        nombre = st.text_input("Nombre del producto")
        fragancia = st.text_input("Fragancia")
        cantidad = st.number_input("Cantidad (ml)", min_value=10, step=10)
        precio = st.number_input("Precio", min_value=0.0, step=1000.0)
        disponible = st.checkbox("¿Disponible?", value=True)
        submit = st.form_submit_button("Guardar loción")

        if submit:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO productos (nombre, fragancia, cantidad_ml, precio, disponible)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre.strip(), fragancia.strip(), cantidad, precio, disponible))
                conexion.commit()
                conexion.close()
                st.success("✅ Loción agregada con éxito.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                
elif opcion == "Agregar compra":
    st.subheader("🛒 Registrar una nueva compra")

    # Conexión y carga de clientes
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
    clientes = cursor.fetchall()

    # Conexión y carga de productos
    cursor.execute("SELECT id, nombre, precio FROM productos ORDER BY nombre")
    productos = cursor.fetchall()

    conexion.close()

    # Convertir a diccionarios para selección
    opciones_clientes = {f"{nombre} (ID {id})": id for id, nombre in clientes}
    opciones_productos = {f"{nombre} - ${float(precio)}": (id, precio) for id, nombre, precio in productos}

    cliente_seleccionado = st.selectbox("👤 Selecciona un cliente", list(opciones_clientes.keys()))
    producto_seleccionado = st.selectbox("🧴 Selecciona una loción", list(opciones_productos.keys()))

    if cliente_seleccionado and producto_seleccionado:
        cliente_id = opciones_clientes[cliente_seleccionado]
        producto_id, precio = opciones_productos[producto_seleccionado]

        confirmar = st.button("💾 Registrar compra")
        if confirmar:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO compras (cliente_id, producto, valor, fecha)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                """, (cliente_id, producto_seleccionado.split(" - ")[0], precio))
                conexion.commit()
                conexion.close()
                st.success("✅ Compra registrada con éxito.")
            except Exception as e:
                st.error(f"❌ Error al registrar la compra: {e}")

elif opcion == "Ver compras":
    st.subheader("🧾 Reporte de Compras")

    conexion = conectar()
    cursor = conexion.cursor()

    # Clientes
    cursor.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
    clientes = cursor.fetchall()
    opciones_clientes = {f"{nombre} (ID {id})": id for id, nombre in clientes}
    opciones_clientes["Todos"] = None

    cliente_seleccionado = st.selectbox("👤 Filtrar por cliente:", list(opciones_clientes.keys()))
    cliente_id = opciones_clientes[cliente_seleccionado]

    # Fechas mínimas y máximas
    cursor.execute("SELECT MIN(fecha), MAX(fecha) FROM compras")
    fecha_min, fecha_max = cursor.fetchone()

    fecha_inicio = st.date_input("📅 Desde:", fecha_min)
    fecha_fin = st.date_input("📅 Hasta:", fecha_max)

    # Consulta dinámica
    sql = """
        SELECT c.nombre, co.producto, co.valor, co.fecha
        FROM clientes c
        INNER JOIN compras co ON c.id = co.cliente_id
        WHERE co.fecha BETWEEN %s AND %s
    """
    valores = [fecha_inicio, fecha_fin]

    if cliente_id:
        sql += " AND c.id = %s"
        valores.append(cliente_id)

    sql += " ORDER BY co.fecha DESC"

    cursor.execute(sql, valores)
    compras = cursor.fetchall()
    conexion.close()

    df = pd.DataFrame(compras, columns=["Cliente", "Producto", "Valor", "Fecha"])
    st.dataframe(df, use_container_width=True)

    total = df["Valor"].sum()
    st.markdown(f"**🧾 Total de compras:** {len(df)}")
    st.markdown(f"**💰 Total gastado:** ${total:,.2f}")

    # 🎨 Gráfico de compras por fecha
    if not df.empty:
        st.markdown("---")
        st.subheader("📈 Gráfico: Total gastado por día")

        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
        resumen = df.groupby("Fecha")["Valor"].sum()

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()
        resumen.plot(kind="line", marker="o", ax=ax)
        ax.set_ylabel("Total gastado")
        ax.set_xlabel("Fecha")
        ax.set_title("Evolución de compras")
        ax.grid(True)

        st.pyplot(fig)