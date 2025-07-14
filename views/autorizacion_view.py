# views/autorizacion_view.py

import streamlit as st
from database.connection import obtener_conexion_cursor

def mostrar_autorizacion_usuarios():
    st.title("🔐 Autorizar nuevos usuarios")

    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT id, nombre, correo, rol
            FROM usuarios
            WHERE autorizado = false AND rol IN ('empleado', 'administrador')
            ORDER BY creado_en DESC;
        """)
        pendientes = cursor.fetchall()
        conexion.close()

        if pendientes:
            for uid, nombre, correo, rol in pendientes:
                with st.expander(f"{nombre} ({rol}) - {correo}"):
                    if st.button(f"✅ Autorizar {nombre}", key=f"auth_{uid}"):
                        try:
                            conn2, cur2 = obtener_conexion_cursor()
                            cur2.execute("UPDATE usuarios SET autorizado = true WHERE id = %s", (uid,))
                            conn2.commit()
                            conn2.close()
                            st.success(f"✅ Usuario autorizado: {nombre}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al autorizar: {e}")
        else:
            st.info("No hay usuarios pendientes por autorizar.")

    except Exception as e:
        st.error(f"❌ Error al cargar usuarios: {e}")