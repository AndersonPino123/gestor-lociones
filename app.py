
import streamlit as st
import psycopg2
import pandas as pd
from datetime import date
from usuarios.usuarios import registrar_usuario, iniciar_sesion

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

def obtener_clientes_activos():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE activo = true ORDER BY nombre")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

def obtener_productos_disponibles():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, genero
        FROM productos
        WHERE disponible = true
        ORDER BY nombre_producto
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

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

# Menú lateral solo si está logueado
if st.session_state.usuario:
    rol = st.session_state.usuario["rol"]
    if rol in ["administrador", "empleado"]:
        st.sidebar.title("🗂️ Navegación")
        opciones = ["Registrar compra"]
        seleccion = st.sidebar.radio("Ir a:", opciones)

        if seleccion == "Registrar compra":
            st.title("🛒 Registrar nueva compra")

            clientes = obtener_clientes_activos()
            if clientes:
                lista = [f"{id} - {nombre}" for id, nombre in clientes]
                seleccion_cliente = st.selectbox("Selecciona el cliente:", lista)
                cliente_id = int(seleccion_cliente.split(" - ")[0])
            else:
                st.warning("⚠️ No hay clientes activos.")
                cliente_id = None

            productos = obtener_productos_disponibles()
            if productos:
                opciones = [
                    f"{id} - {marca} | {nombre} ({genero.capitalize()})"
                    for id, marca, nombre, genero in productos
                ]
                seleccion_prod = st.selectbox("Selecciona el producto comprado:", opciones)
                producto = seleccion_prod.split(" - ", 1)[1]
            else:
                st.warning("⚠️ No hay productos disponibles.")
                producto = None

            valor = st.number_input("Valor del producto", min_value=0.0, step=1000.0)

            if st.button("💾 Guardar compra"):
                if not cliente_id:
                    st.warning("Debes seleccionar un cliente válido.")
                elif not producto:
                    st.warning("Debes seleccionar un producto válido.")
                else:
                    try:
                        conexion, cursor = obtener_conexion_cursor()
                        cursor.execute(
                            "INSERT INTO compras (cliente_id, producto, valor, fecha) VALUES (%s, %s, %s, CURRENT_DATE)",
                            (cliente_id, producto, valor)
                        )
                        conexion.commit()
                        conexion.close()
                        st.success("✅ Compra registrada con éxito.")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    else:
        st.title("🛍️ Catálogo de Lociones")
        st.info("Aquí irá el catálogo para los clientes.")
else:
    st.title("🛍️ Catálogo de Lociones")
    st.info("Aquí irá el catálogo para visitantes no registrados.")
