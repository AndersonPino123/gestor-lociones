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

# ✅ Mostrar catálogo con formato visual bonito
def ver_catalogo(filtro):
    conexion = conectar()
    cursor = conexion.cursor()
    if filtro == "Todos":
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url
            FROM productos WHERE disponible = true ORDER BY nombre_producto;
        """)
    else:
        cursor.execute("""
            SELECT marca, nombre_producto, fragancia, cantidad_ml, precio, imagen_url
            FROM productos WHERE disponible = true AND genero = %s ORDER BY nombre_producto;
        """, (filtro.lower(),))
    productos = cursor.fetchall()
    conexion.close()
    return productos

# ✅ Mostrar clientes activos
def ver_clientes():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("SELECT id, nombre FROM clientes WHERE activo = true ORDER BY nombre")
    clientes = cursor.fetchall()
    conexion.close()
    return clientes

# ✅ Mostrar productos disponibles para registrar compra
def ver_productos_disponibles():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute("""
        SELECT id, marca, nombre_producto, genero FROM productos
        WHERE disponible = true ORDER BY nombre_producto
    """)
    productos = cursor.fetchall()
    conexion.close()
    return productos

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
                # Registro adicional en la tabla clientes
                try:
                    conexion, cursor = obtener_conexion_cursor()
                    cursor.execute("""
                        INSERT INTO clientes (nombre, correo, edad, activo, creado_en)
                        VALUES (%s, %s, %s, %s, CURRENT_DATE)
                    """, (nombre, correo, 0, True))
                    conexion.commit()
                    conexion.close()
                except Exception as e:
                    st.warning(f"⚠️ Registro incompleto en tabla clientes: {e}")
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- MENÚ CATÁLOGO -------------------- #
menu = st.sidebar.selectbox("🗂️ Navegación", ["Catálogo", "Registrar compra"])

if menu == "Catálogo":
    st.title("🛍️ Catálogo de Lociones")
    filtro_genero = st.sidebar.selectbox("Filtrar por género", ["Todos", "Femenino", "Masculino"])
    productos = ver_catalogo(filtro_genero)
    if productos:
        for marca, nombre, fragancia, cantidad, precio, imagen in productos:
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(imagen or "https://via.placeholder.com/150", width=120)
                with cols[1]:
                    st.subheader(f"{nombre}")
                    st.markdown(f"- 🏷️ Marca: {marca}")
                    st.markdown(f"- 🌸 Fragancia: {fragancia}")
                    st.markdown(f"- 🧪 {cantidad} ml")
                    st.markdown(f"- 💰 ${precio:,.0f}")
                    st.markdown("---")
    else:
        st.info("No hay productos disponibles.")

# -------------------- REGISTRAR COMPRA -------------------- #
el_rol = st.session_state.usuario["rol"] if st.session_state.usuario else None
if menu == "Registrar compra" and el_rol in ["empleado", "administrador"]:
    st.title("🛒 Registrar Compra")

    clientes = ver_clientes()
    productos = ver_productos_disponibles()

    if not clientes:
        st.warning("⚠️ No hay clientes activos.")
    elif not productos:
        st.warning("⚠️ No hay productos disponibles.")
    else:
        lista_clientes = [f"{id} - {nombre}" for id, nombre in clientes]
        lista_productos = [f"{id} - {marca} {nombre} ({genero})" for id, marca, nombre, genero in productos]

        seleccion_cliente = st.selectbox("Selecciona el cliente:", lista_clientes)
        cliente_id = int(seleccion_cliente.split(" - ")[0])

        seleccion_producto = st.selectbox("Selecciona el producto:", lista_productos)
        producto_nombre = seleccion_producto.split(" - ", 1)[1]  # Lo que se muestra

        valor = st.number_input("Valor del producto", min_value=0.0, step=1000.0)

        if st.button("💾 Guardar compra"):
            try:
                conexion, cursor = obtener_conexion_cursor()
                cursor.execute("""
                    INSERT INTO compras (cliente_id, producto, valor, fecha)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                """, (cliente_id, producto_nombre, valor))
                conexion.commit()
                conexion.close()
                st.success("✅ Compra registrada correctamente.")
            except Exception as e:
                st.error(f"❌ Error al registrar compra: {e}")