# views/menu.py

import streamlit as st

def mostrar_menu_usuario(rol):
    if rol == "administrador":
        return st.sidebar.selectbox("🗂️ Navegación", [
            "Catálogo", "Clientes", "Lociones", "Registrar compra",
            "Resumen de ventas", "Compras por cliente", "Gráfico de ventas",
            "Autorizar usuarios", "Gestionar roles"
        ])
    elif rol == "empleado":
        return st.sidebar.selectbox("🗂️ Navegación", [
            "Catálogo", "Clientes", "Registrar compra"
        ])
    else:  # cliente
        return st.sidebar.selectbox("🗂️ Navegación", ["Catálogo"])

def mostrar_menu_visitante():
    return "Catálogo"