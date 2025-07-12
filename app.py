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

def obtener_conexion_cursor():
    conexion = conectar()
    cursor = conexion.cursor()
    return conexion, cursor

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
                
if menu == "Lociones":
    st.title("🧴 Lista de Lociones")
    df = ver_productos()
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("➕ Agregar nueva loción")

    with st.form("form_locion"):
        marca = st.text_input("Marca")
        nombre_producto = st.text_input("Nombre del producto")
        ref_proveedor = st.text_input("Referencia con proveedor")
        fragancia = st.text_input("Fragancia")
        genero = st.selectbox("Género", ["femenino", "masculino"])
        cantidad = st.number_input("Cantidad (ml)", min_value=10, step=10)
        precio = st.number_input("Precio", min_value=0.0, step=1000.0)
        stock = st.number_input("Stock", min_value=0, step=1)
        disponible = st.checkbox("¿Disponible?", value=True)
        imagen_url = st.text_input("URL de imagen (opcional)")

        submit = st.form_submit_button("Guardar loción")

        if submit:
            try:
                conexion = conectar()
                cursor = conexion.cursor()
                cursor.execute("""
                    INSERT INTO productos (
                        marca, nombre_producto, ref_proveedor, genero, fragancia,
                        cantidad_ml, precio, stock, disponible, imagen_url, fecha_creacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
                """, (marca, nombre_producto, ref_proveedor, genero, fragancia,
                      cantidad, precio, stock, disponible, imagen_url))
                conexion.commit()
                conexion.close()
                st.success("✅ Loción agregada con éxito.")
            except Exception as e:
                st.error(f"❌ Error al guardar: {e}")
                
# -------------------- PANEL ADMINISTRADOR -------------------- #
if menu == "Resumen de ventas":
    st.title("📊 Resumen de ventas del mes")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT SUM(valor) FROM compras
            WHERE DATE_PART('month', fecha) = DATE_PART('month', CURRENT_DATE)
            AND DATE_PART('year', fecha) = DATE_PART('year', CURRENT_DATE);
        """)
        total = cursor.fetchone()[0] or 0
        st.metric("💰 Total de ventas del mes", f"${total:,.0f}")
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al obtener el resumen: {e}")

elif menu == "Compras por cliente":
    st.title("👥 Compras por Cliente")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT c.nombre, COUNT(co.id) AS cantidad, SUM(co.valor) AS total
            FROM clientes c
            JOIN compras co ON c.id = co.cliente_id
            GROUP BY c.nombre
            ORDER BY total DESC;
        """)
        resultados = cursor.fetchall()
        df = pd.DataFrame(resultados, columns=["Cliente", "Compras", "Total gastado"])
        st.dataframe(df, use_container_width=True)
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al consultar compras por cliente: {e}")

elif menu == "Gráfico de ventas":
    st.title("📈 Gráfico de Ventas por Fecha")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT fecha, SUM(valor) AS total
            FROM compras
            GROUP BY fecha
            ORDER BY fecha;
        """)
        datos = cursor.fetchall()
        df = pd.DataFrame(datos, columns=["Fecha", "Total"])
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        st.line_chart(df.set_index("Fecha"))
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al generar el gráfico: {e}")