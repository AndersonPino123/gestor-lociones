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

# -------------------- FUNCIONES BÁSICAS -------------------- #
def obtener_conexion_cursor():
    conexion = conectar()
    cursor = conexion.cursor()
    return conexion, cursor

def obtener_productos_disponibles():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("SELECT id, marca, nombre_producto, genero FROM productos WHERE disponible = true ORDER BY nombre_producto;")
    datos = cursor.fetchall()
    conexion.close()
    return datos

def obtener_clientes_activos():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE activo = true ORDER BY nombre")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

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
        if st.sidebar.button("📝 Registrarse"):
            rol = "cliente"
            if registrar_usuario(nombre, correo, contrasena, rol):
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- MENÚ -------------------- #
menu = "Catálogo"
if st.session_state.usuario:
    rol = st.session_state.usuario["rol"]
    if rol == "administrador":
        menu = st.sidebar.selectbox("🗂️ Navegación", [
            "Catálogo", "Clientes", "Lociones", "Registrar compra",
            "Resumen de ventas", "Compras por cliente", "Gráfico de ventas",
            "Autorizar usuarios", "Gestionar roles"
        ])
    elif rol == "empleado":
        menu = st.sidebar.selectbox("🗂️ Navegación", [
            "Catálogo", "Clientes", "Registrar compra"
        ])

# -------------------- CATÁLOGO -------------------- #
if menu == "Catálogo":
    st.title("🛍️ Catálogo de Lociones")
    filtro = st.sidebar.selectbox("Filtrar por género", ["Todos", "Femenino", "Masculino"])
    conexion, cursor = obtener_conexion_cursor()
    if filtro == "Todos":
        cursor.execute("SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url FROM productos WHERE disponible = true")
    else:
        cursor.execute("SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url FROM productos WHERE disponible = true AND genero = %s", (filtro.lower(),))
    productos = cursor.fetchall()
    conexion.close()

    for marca, nombre, fragancia, cantidad, precio, imagen_url in productos:
        with st.container():
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(imagen_url or "https://via.placeholder.com/120", width=120)
            with cols[1]:
                st.markdown(f"### {nombre}")
                st.markdown(f"**Marca:** {marca}")
                st.markdown(f"**Fragancia:** {fragancia}")
                st.markdown(f"**Cantidad:** {cantidad} ml")
                st.markdown(f"**Precio:** ${precio:,.0f}")
                st.markdown("---")

# -------------------- REGISTRAR COMPRA -------------------- #
if menu == "Registrar compra" and st.session_state.usuario["rol"] in ["empleado", "administrador"]:
    st.title("🛒 Registrar nueva compra")
    clientes = obtener_clientes_activos()
    if clientes:
        seleccion = st.selectbox("Selecciona el cliente:", [f"{id} - {nombre}" for id, nombre in clientes])
        cliente_id = int(seleccion.split(" - ")[0])
    else:
        st.warning("⚠️ No hay clientes activos.")
        cliente_id = None

    productos_disponibles = obtener_productos_disponibles()
    if productos_disponibles:
        opciones = [f"{id} - {marca} | {nombre} ({genero})" for id, marca, nombre, genero in productos_disponibles]
        seleccion_producto = st.selectbox("Selecciona el producto comprado", opciones)
        producto = seleccion_producto.split(" - ", 1)[1]
    else:
        st.warning("⚠️ No hay productos disponibles.")
        producto = None

    valor = st.number_input("Valor del producto", min_value=0.0, step=1000.0)
    if st.button("💾 Guardar compra"):
        if not cliente_id:
            st.warning("Selecciona un cliente válido.")
        elif not producto:
            st.warning("Selecciona un producto.")
        else:
            try:
                conexion, cursor = obtener_conexion_cursor()
                cursor.execute("INSERT INTO compras (cliente_id, producto, valor, fecha) VALUES (%s, %s, %s, CURRENT_DATE)", (cliente_id, producto, valor))
                conexion.commit()
                conexion.close()
                st.success("✅ Compra registrada.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
