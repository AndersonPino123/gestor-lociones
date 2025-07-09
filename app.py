import streamlit as st
import psycopg2
import pandas as pd
from datetime import date

# ✅ Conexión usando secrets
def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

# ✅ Función para ver catálogo
def ver_catalogo(filtro):
    conexion = conectar()
    cursor = conexion.cursor()

    if filtro == "Todos":
        cursor.execute("""
            SELECT nombre, fragancia, cantidad_ml, precio, disponible, imagen_url
            FROM productos
            WHERE disponible = true
            ORDER BY nombre;
        """)
    else:
        cursor.execute("""
            SELECT nombre, fragancia, cantidad_ml, precio, disponible, imagen_url
            FROM productos
            WHERE disponible = true AND genero = %s
            ORDER BY nombre;
        """, (filtro.lower(),))

    productos = cursor.fetchall()
    conexion.close()
    return productos

# ✅ Función para mostrar clientes
def ver_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, edad, activo, creado_en FROM clientes ORDER BY id")
    datos = cursor.fetchall()
    columnas = ["ID", "Nombre", "Correo", "Edad", "Activo", "Creado en"]
    df = pd.DataFrame(datos, columns=columnas)
    conexion.close()
    return df

# ✅ Función para mostrar lociones (modo admin)
def ver_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, ref_proveedor, genero, fragancia,
               cantidad_ml, precio, stock, disponible, fecha_creacion, imagen_url
        FROM productos ORDER BY id
    """)
    datos = cursor.fetchall()
    columnas = ["ID", "Marca", "Nombre", "Referencia proveedor", "Género", "Fragancia",
                "Cantidad (ml)", "Precio", "Stock", "Disponible", "Fecha", "Imagen"]
    df = pd.DataFrame(datos, columns=columnas)
    conexion.close()
    return df

# 🎯 Sidebar para navegación
opcion = st.sidebar.selectbox("📂 Menú", ["Catálogo", "Clientes", "Lociones"])

# 🛍️ CATÁLOGO DE LOCIONES (VISITANTES)
if opcion == "Catálogo":
    st.title("🛍️ Catálogo de Lociones")
    st.sidebar.markdown("## 🧴 Filtrar por género")
    filtro_genero = st.sidebar.selectbox("Selecciona:", ["Todos", "Femenino", "Masculino"])

    productos = ver_catalogo(filtro_genero)

    for producto in productos:
        nombre, fragancia, cantidad, precio, disponible, imagen_url = producto

        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                if imagen_url:
                    st.image(imagen_url, width=120)
                else:
                    st.image("https://via.placeholder.com/120", caption="Sin imagen")
            with cols[1]:
                st.markdown(f"### {nombre}")
                st.markdown(f"- 🌸 Fragancia: {fragancia}")
                st.markdown(f"- 🧪 Cantidad: {cantidad} ml")
                st.markdown(f"- 💰 Precio: ${precio:,.0f}")
                st.markdown("---")

# 👥 CLIENTES
elif opcion == "Clientes":
    st.subheader("👥 Lista de Clientes")
    st.dataframe(ver_clientes(), use_container_width=True)

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

# 🧴 LOCIONES (modo administrador)
elif opcion == "Lociones":
    st.subheader("🧴 Lista de Lociones")
    st.dataframe(ver_productos(), use_container_width=True)

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