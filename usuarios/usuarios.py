import psycopg2
import hashlib
from datetime import date
import streamlit as st

# Conexión a Supabase (desde secrets)
def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

# Función para encriptar contraseña (usando SHA256)
def encriptar_contrasena(contra):
    return hashlib.sha256(contra.encode()).hexdigest()

# Registrar nuevo usuario
def registrar_usuario(nombre, correo, contrasena, rol):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        hash_pw = encriptar_contrasena(contrasena)

        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contrasena, rol, creado_en)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, correo, hash_pw, rol, date.today()))

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al registrar: {e}")
        return False

# Iniciar sesión
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

        hash_ingresada = encriptar_contrasena(contrasena)

        if usuario and usuario[2] == hash_ingresada:
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