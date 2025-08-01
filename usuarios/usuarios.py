import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import streamlit as st

def conectar():
    return psycopg2.connect(
        host=st.secrets["database"]["host"],
        port=st.secrets["database"]["port"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"]
    )

def registrar_usuario(nombre, correo, contrasena, rol):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        hash_pw = generate_password_hash(contrasena)

        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, contrasena, rol, creado_en)
            VALUES (%s, %s, %s, %s, CURRENT_DATE)
        """, (nombre, correo, hash_pw, rol))
        conexion.commit()

        if rol == "cliente":
            try:
                cursor.execute("""
                    INSERT INTO clientes (nombre, correo, edad, activo, creado_en)
                    VALUES (%s, %s, %s, true, CURRENT_DATE)
                """, (nombre, correo, 0))
                conexion.commit()
            except Exception as e:
                st.error(f"❌ Error al crear el cliente: {e}")

        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al registrar: {e}")
        return False

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