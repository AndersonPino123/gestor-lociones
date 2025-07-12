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

# ✅ Función para actualizar cliente
def actualizar_cliente(id_cliente, nuevo_nombre, nuevo_correo, nueva_edad):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE clientes SET nombre=%s, correo=%s, edad=%s
        WHERE id=%s
    """, (nuevo_nombre, nuevo_correo, nueva_edad, id_cliente))
    conexion.commit()
    conexion.close()

# ✅ Función para cambiar estado (activo/inactivo)
def cambiar_estado_cliente(id_cliente, nuevo_estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE clientes SET activo=%s WHERE id=%s", (nuevo_estado, id_cliente))
    conexion.commit()
    conexion.close()

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

# 👥 CLIENTES
if menu == "Clientes":
    st.title("👥 Gestión de Clientes")
    df = ver_clientes()
    st.dataframe(df, use_container_width=True)

    with st.expander("➕ Agregar nuevo cliente"):
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

    st.markdown("---")
    st.subheader("✏️ Editar o cambiar estado de clientes")

    for _, fila in df.iterrows():
        with st.expander(f"👤 {fila['Nombre']} ({'Activo' if fila['Activo'] else 'Inactivo'})"):
            nuevo_nombre = st.text_input("Nombre", fila["Nombre"], key=f"nombre_{fila['ID']}")
            nuevo_correo = st.text_input("Correo", fila["Correo"], key=f"correo_{fila['ID']}")
            nueva_edad = st.number_input("Edad", value=fila["Edad"], min_value=0, max_value=120, step=1, key=f"edad_{fila['ID']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Guardar cambios", key=f"guardar_{fila['ID']}"):
                    actualizar_cliente(fila['ID'], nuevo_nombre, nuevo_correo, nueva_edad)
                    st.success("✅ Cambios guardados. Recarga para ver reflejado.")
            with col2:
                if fila['Activo']:
                    if st.button("🚫 Desactivar", key=f"desactivar_{fila['ID']}"):
                        cambiar_estado_cliente(fila['ID'], False)
                        st.warning("⚠️ Cliente desactivado. Recarga para ver reflejado.")
                else:
                    if st.button("✅ Activar", key=f"activar_{fila['ID']}"):
                        cambiar_estado_cliente(fila['ID'], True)
                        st.success("✅ Cliente activado. Recarga para ver reflejado.")

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