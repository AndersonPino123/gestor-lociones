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
    cursor.execute("""
        SELECT id, marca, nombre_producto, genero
        FROM productos
        WHERE disponible = true
        ORDER BY nombre_producto
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

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
                st.session_state.usuario = usuario
                st.success(f"¡Bienvenido, {usuario['nombre']}! 👋")
                st.rerun()
            else:
                st.error("Correo o contraseña incorrectos o no autorizado.")
    else:
        nombre = st.sidebar.text_input("Nombre", key="reg_nombre")
        correo = st.sidebar.text_input("Correo", key="reg_correo")
        contrasena = st.sidebar.text_input("Contraseña", type="password", key="reg_contra")
        if st.sidebar.button("📝 Registrarse"):
            if registrar_usuario(nombre, correo, contrasena, rol="cliente"):
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- MENÚ SEGÚN ROL -------------------- #
if st.session_state.usuario:
    rol = st.session_state.usuario["rol"]
    if rol == "administrador":
        menu = st.sidebar.selectbox("⚙️ Menú", [
            "Catálogo", "Registrar compra", "Resumen de ventas",
            "Compras por cliente", "Gráfico de ventas", "Autorizar usuarios"
        ])
    elif rol == "empleado":
        menu = st.sidebar.selectbox("📋 Menú", ["Catálogo", "Registrar compra"])
    else:
        menu = st.sidebar.selectbox("🛍️ Menú", ["Catálogo"])
else:
    menu = st.sidebar.selectbox("🛍️ Menú Visitante", ["Catálogo"])

# -------------------- CATÁLOGO -------------------- #
if menu == "Catálogo":
    st.title("🛍️ Catálogo de Lociones")
    productos = obtener_productos_disponibles()
    if productos:
        for _, marca, nombre, genero in productos:
            st.markdown(f"- **{marca} {nombre}** ({genero})")
    else:
        st.info("No hay productos disponibles.")

# -------------------- REGISTRAR COMPRA -------------------- #
if menu == "Registrar compra" and st.session_state.usuario["rol"] in ["empleado", "administrador"]:
    st.title("🛒 Registrar compra")

    clientes = obtener_clientes_activos()
    if clientes:
        cliente_opciones = [f"{id} - {nombre}" for id, nombre in clientes]
        seleccion_cliente = st.selectbox("Selecciona cliente:", cliente_opciones)
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
        seleccion_producto = st.selectbox("Selecciona producto:", opciones)
        producto = seleccion_producto.split(" - ", 1)[1]
    else:
        st.warning("⚠️ No hay productos disponibles.")
        producto = None

    valor = st.number_input("Valor del producto", min_value=0.0, step=1000.0)

    if st.button("💾 Guardar compra"):
        if not cliente_id or not producto:
            st.warning("Debes seleccionar cliente y producto.")
        else:
            try:
                conexion, cursor = obtener_conexion_cursor()
                cursor.execute("""
                    INSERT INTO compras (cliente_id, producto, valor, fecha)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                """, (cliente_id, producto, valor))
                conexion.commit()
                conexion.close()
                st.success("✅ Compra registrada.")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# -------------------- ADMIN: AUTORIZAR USUARIOS -------------------- #
if menu == "Autorizar usuarios" and st.session_state.usuario["rol"] == "administrador":
    st.title("🔐 Autorizar usuarios")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT id, nombre, correo, rol FROM usuarios
            WHERE autorizado = false AND rol IN ('empleado', 'administrador')
            ORDER BY creado_en DESC
        """)
        pendientes = cursor.fetchall()
        conexion.close()

        if pendientes:
            for uid, nombre, correo, rol in pendientes:
                with st.expander(f"{nombre} ({rol}) - {correo}"):
                    if st.button(f"✅ Autorizar", key=f"auth_{uid}"):
                        try:
                            conn2, cur2 = obtener_conexion_cursor()
                            cur2.execute("UPDATE usuarios SET autorizado = true WHERE id = %s", (uid,))
                            conn2.commit()
                            conn2.close()
                            st.success(f"✅ Usuario autorizado.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al autorizar: {e}")
        else:
            st.info("No hay usuarios pendientes.")
    except Exception as e:
        st.error(f"❌ Error al cargar usuarios: {e}")
