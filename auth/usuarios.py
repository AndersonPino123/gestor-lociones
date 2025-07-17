# auth/usuarios.py

import psycopg2
import streamlit as st
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import conectar


# ✅ Registrar nuevo usuario
def registrar_usuario(nombre, correo, contrasena, rol):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        hash_pw = generate_password_hash(contrasena)
        autorizado = rol == "cliente"  # Solo los clientes quedan autorizados de una

        cursor.execute(
            """
            INSERT INTO usuarios (nombre, correo, contrasena, rol, autorizado, creado_en)
            VALUES (%s, %s, %s, %s, %s, %s)
        """,
            (nombre, correo, hash_pw, rol, autorizado, date.today()),
        )

        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al registrar: {e}")
        return False


# ✅ Iniciar sesión
def iniciar_sesion(correo, contrasena):
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id, nombre, correo, contrasena, rol, autorizado
            FROM usuarios WHERE correo = %s
        """,
            (correo,),
        )
        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario[3], contrasena):
            if usuario[5] or usuario[4] == "cliente":
                return {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "correo": usuario[2],  # 👈 AÑADIR ESTA LÍNEA
                    "rol": usuario[4],
                }
            else:
                st.warning(
                    "⚠️ Tu cuenta aún no ha sido autorizada por un administrador."
                )
        return None
    except Exception as e:
        st.error(f"❌ Error al iniciar sesión: {e}")
        return None


# ✅ Obtener usuarios pendientes por autorizar
def obtener_usuarios_pendientes():
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute(
        """
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE autorizado = false AND rol IN ('empleado', 'administrador')
        ORDER BY creado_en DESC;
    """
    )
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


# ✅ Autorizar usuario
def autorizar_usuario(user_id):
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            "UPDATE usuarios SET autorizado = true WHERE id = %s", (user_id,)
        )
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al autorizar usuario: {e}")
        return False


# ✅ Obtener usuarios autorizados (excepto tú mismo)
def obtener_usuarios_autorizados(excluir_correo):
    conexion, cursor = obtener_conexion_cursor()
    cursor.execute(
        """
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE autorizado = true AND correo != %s
        ORDER BY nombre
    """,
        (excluir_correo,),
    )
    usuarios = cursor.fetchall()
    conexion.close()
    return usuarios


# ✅ Cambiar rol de un usuario
def cambiar_rol_usuario(user_id, nuevo_rol):
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            "UPDATE usuarios SET rol = %s WHERE id = %s", (nuevo_rol, user_id)
        )
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        st.error(f"❌ Error al cambiar rol: {e}")
        return False


# ✅ Obtener conexión desde módulo database
def obtener_conexion_cursor():
    conexion = conectar()
    cursor = conexion.cursor()
    return conexion, cursor
