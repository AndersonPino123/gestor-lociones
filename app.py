# app.py

import streamlit as st
import pandas as pd
from datetime import date

from auth.usuarios import registrar_usuario, iniciar_sesion
from database.connection import obtener_conexion_cursor
from views.menu import mostrar_menu_visitante, mostrar_menu_usuario
from views.catalogo_view import mostrar_catalogo
from views.clientes_view import mostrar_gestion_clientes
from views.lociones_view import mostrar_gestion_lociones
from views.compras_view import mostrar_registro_compra
from views.panel_admin import mostrar_resumen_ventas, mostrar_compras_por_cliente
from views.graficos import mostrar_grafico_lineas
from views.autorizacion_view import mostrar_autorizacion_usuarios
from views.roles_view import mostrar_gestion_roles

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
                st.success("✅ Registro exitoso. Ahora inicia sesión.")
else:
    usuario = st.session_state.usuario
    st.sidebar.success(f"Sesión activa: {usuario['nombre']} ({usuario['rol']})")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.usuario = None
        st.rerun()

# -------------------- MENÚ -------------------- #
if st.session_state.usuario:
    menu = mostrar_menu_usuario(st.session_state.usuario["rol"])
else:
    menu = mostrar_menu_visitante()

# -------------------- NAVEGACIÓN -------------------- #
if menu == "Catálogo":
    mostrar_catalogo()

elif menu == "Clientes":
    mostrar_gestion_clientes()

elif menu == "Lociones":
    mostrar_gestion_lociones()

elif menu == "Registrar compra":
    mostrar_registro_compra()

elif menu == "Resumen de ventas":
    mostrar_resumen_ventas()

elif menu == "Compras por cliente":
    mostrar_compras_por_cliente()

elif menu == "Gráfico de ventas":
    mostrar_grafico_lineas()

elif menu == "Autorizar usuarios":
    mostrar_autorizacion_usuarios()

elif menu == "Gestionar roles":
    mostrar_gestion_roles()