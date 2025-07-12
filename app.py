import streamlit as st
import psycopg2
import pandas as pd
from datetime import date
from usuarios.usuarios import registrar_usuario, iniciar_sesion

# -------------------- CONEXIÓN -------------------- #
def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

# -------------------- CONSULTAS -------------------- #
def ver_catalogo(filtro):
    conexion = conectar()
    cursor = conexion.cursor()
    if filtro == "Todos":
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, disponible, imagen_url
            FROM productos WHERE disponible = true ORDER BY nombre_producto;
        """)
    else:
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, disponible, imagen_url
            FROM productos WHERE disponible = true AND genero = %s ORDER BY nombre_producto;
        """, (filtro.lower(),))
    productos = cursor.fetchall()
    conexion.close()
    return productos

def ver_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo, edad, activo, creado_en FROM clientes ORDER BY id")
    datos = cursor.fetchall()
    conexion.close()
    return pd.DataFrame(datos, columns=["ID", "Nombre", "Correo", "Edad", "Activo", "Creado en"])

def ver_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, ref_proveedor, genero, fragancia,
               cantidad_ml, precio, stock, disponible, fecha_creacion, imagen_url
        FROM productos ORDER BY id
    """)
    datos = cursor.fetchall()
    conexion.close()
    columnas = ["ID", "Marca", "Nombre", "Referencia proveedor", "Género", "Fragancia",
                "Cantidad (ml)", "Precio", "Stock", "Disponible", "Fecha", "Imagen"]
    return pd.DataFrame(datos, columns=columnas)

# -------------------- AUTENTICACIÓN -------------------- #
st.sidebar.markdown("## 🔐 Iniciar sesión o registrarse")
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if st.session_state.usuario is None:
    opcion = st.sidebar.radio("¿Qué quieres hacer?", ["Iniciar sesión", "Registrarse"])
    if opcion == "Iniciar sesión":
        correo = st.sidebar.text_input("Correo", key="login_correo")
        contrasena = st.sidebar.text_input("Contraseña", type="password", key="login_contra")
        if st.sidebar.button("🔓 Iniciar sesión"):
            usuario = iniciar_sesion(correo, contrasena)
            if usuario:
                st.success(f"¡Bienvenido, {usuario['nombre']}! 👋")
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos.")
    else:
        nombre = st.sidebar.text_input("Nombre", key="reg_nombre")
        correo = st.sidebar.text_input("Correo", key="reg_correo")
        contrasena = st.sidebar.text_input("Contraseña", type="password", key="reg_contra")
        rol = st.sidebar.selectbox("Rol", ["cliente", "empleado", "administrador"])
        if st.sidebar.button("📝 Registrarse"):
            if registrar_usuario(nombre, correo, contrasena, rol):
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- MENÚ -------------------- #
if st.session_state.usuario:
    rol = st.session_state.usuario["rol"]
    if rol == "administrador":
        menu = st.sidebar.selectbox("⚙️ Menú Administrador", [
            "Catálogo", "Clientes", "Lociones", "Resumen de ventas", "Compras por cliente", "Gráfico de ventas"
        ])
    elif rol == "empleado":
        menu = st.sidebar.selectbox("📋 Menú Empleado", ["Catálogo", "Clientes", "Registrar compra"])
    else:
        menu = st.sidebar.selectbox("🛍️ Menú Cliente", ["Catálogo"])
else:
    menu = st.sidebar.selectbox("🛍️ Menú Visitante", ["Catálogo"])

# -------------------- SECCIONES -------------------- #
if menu == "Catálogo":
    st.title("🛍️ Catálogo de Lociones")
    filtro_genero = st.sidebar.selectbox("Filtrar por género", ["Todos", "Femenino", "Masculino"])
    productos = ver_catalogo(filtro_genero)
    for marca, nombre, fragancia, cantidad, precio, disponible, imagen_url in productos:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(imagen_url or "https://via.placeholder.com/120", width=120)
            with cols[1]:
                st.markdown(f"#### 🏷️ Marca: {marca}")
                st.markdown(f"### {nombre}")
                st.markdown(f"- 🌸 Fragancia: {fragancia}")
                st.markdown(f"- 🧪 Cantidad: {cantidad} ml")
                st.markdown(f"- 💰 Precio: ${precio:,.0f}")
                st.markdown("---")