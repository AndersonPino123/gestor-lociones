# views/roles_view.py

import streamlit as st
from database.connection import obtener_conexion_cursor


def mostrar_gestion_roles(usuario_actual):
    st.title("🔁 Cambiar rol de usuarios")

    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            """
            SELECT id, nombre, correo, rol
            FROM usuarios
            WHERE autorizado = true AND correo != %s
            ORDER BY nombre
        """,
            (usuario_actual["correo"],),
        )  # Evita mostrar al usuario actual

        usuarios = cursor.fetchall()
        conexion.close()

        if usuarios:
            for uid, nombre, correo, rol_actual in usuarios:
                with st.expander(f"{nombre} - {correo}"):
                    nuevo_rol = st.selectbox(
                        "Selecciona el nuevo rol:",
                        ["cliente", "empleado", "administrador"],
                        index=["cliente", "empleado", "administrador"].index(
                            rol_actual
                        ),
                        key=f"rol_{uid}",
                    )
                    if nuevo_rol != rol_actual:
                        if st.button("💾 Cambiar rol", key=f"guardar_rol_{uid}"):
                            try:
                                conn2, cur2 = obtener_conexion_cursor()
                                cur2.execute(
                                    "UPDATE usuarios SET rol = %s WHERE id = %s",
                                    (nuevo_rol, uid),
                                )
                                conn2.commit()
                                conn2.close()
                                st.success(
                                    f"✅ Rol actualizado: {nombre} ahora es {nuevo_rol}."
                                )
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error al cambiar rol: {e}")
        else:
            st.info("No hay otros usuarios autorizados para mostrar.")

    except Exception as e:
        st.error(f"❌ Error al cargar usuarios: {e}")
