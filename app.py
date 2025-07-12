
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

def obtener_conexion_cursor():
    conexion = conectar()
    cursor = conexion.cursor()
    return conexion, cursor

# -------------------- CATÁLOGO -------------------- #
def ver_catalogo():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("""
        SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url, genero
        FROM productos WHERE disponible = true ORDER BY nombre_producto;
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

# -------------------- MENÚ -------------------- #
def mostrar_catalogo():
    st.title("🛍️ Catálogo de Lociones")
    productos = ver_catalogo()
    if not productos:
        st.info("No hay productos disponibles.")
    for marca, nombre, fragancia, cantidad, precio, imagen, genero in productos:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(imagen or "https://via.placeholder.com/120", width=120)
            with cols[1]:
                st.markdown(f"### {nombre} ({genero})")
                st.markdown(f"- 🏷️ Marca: {marca}")
                st.markdown(f"- 🌸 Fragancia: {fragancia}")
                st.markdown(f"- 🧪 Cantidad: {cantidad} ml")
                st.markdown(f"- 💰 Precio: ${precio:,.0f}")
                st.markdown("---")

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
                st.session_state.usuario = usuario
                st.success(f"¡Bienvenido, {usuario['nombre']}!")
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos.")
    else:
        nombre = st.sidebar.text_input("Nombre", key="reg_nombre")
        correo = st.sidebar.text_input("Correo", key="reg_correo")
        contrasena = st.sidebar.text_input("Contraseña", type="password", key="reg_contra")
        if st.sidebar.button("📝 Registrarse"):
            if registrar_usuario(nombre, correo, contrasena, "cliente"):
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- NAVEGACIÓN -------------------- #
if st.session_state.usuario:
    rol = st.session_state.usuario["rol"]
    if rol in ["administrador", "empleado"]:
        menu = st.sidebar.selectbox("🗂️ Navegación", ["Catálogo", "Registrar compra"])
    else:
        menu = "Catálogo"
else:
    menu = "Catálogo"

# -------------------- SECCIONES -------------------- #
if menu == "Catálogo":
    mostrar_catalogo()
elif menu == "Registrar compra":
    st.title("🛒 Registrar nueva compra")
    # Aquí irá el formulario completo de registrar compra
    st.info("Funcionalidad pendiente de integrar aquí.")
