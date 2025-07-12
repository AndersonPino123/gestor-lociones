import psycopg2
import streamlit as st
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- CONEXIÓN -------------------- #
def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

# -------------------- REGISTRAR USUARIO -------------------- #
def registrar_usuario(nombre, correo, contrasena, rol="cliente"):
    try:
        hash_pw = generate_password_hash(contrasena)
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contrasena, rol, autorizado, creado_en)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, correo, hash_pw, rol, True if rol == "cliente" else False, date.today()))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al registrar usuario: {e}")
        return False

# -------------------- INICIAR SESIÓN -------------------- #
def iniciar_sesion(correo, contrasena):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, contrasena, rol, autorizado
            FROM usuarios
            WHERE correo = %s
        """, (correo,))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario[2], contrasena):
            if usuario[4] or usuario[3] == "cliente":
                return {"id": usuario[0], "nombre": usuario[1], "rol": usuario[3]}
            else:
                st.warning("⚠️ Tu cuenta aún no ha sido autorizada por un administrador.")
                return None
        else:
            return None
    except Exception as e:
        st.error(f"❌ Error al iniciar sesión: {e}")
        return None