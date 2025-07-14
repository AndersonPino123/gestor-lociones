# utils/helpers.py

import streamlit as st

def mostrar_mensaje_exito(mensaje: str):
    st.success(f"✅ {mensaje}")

def mostrar_mensaje_error(error: Exception, mensaje="Se produjo un error."):
    st.error(f"❌ {mensaje}: {error}")

def mostrar_mensaje_advertencia(mensaje: str):
    st.warning(f"⚠️ {mensaje}")

def formatear_moneda(valor):
    """Formatea un valor numérico como moneda colombiana."""
    return f"${valor:,.0f}".replace(",", ".")

def parsear_id_desde_texto(texto: str):
    """
    Recibe algo como '5 - Juan Pérez' y devuelve 5 como int.
    """
    try:
        return int(texto.split(" - ")[0])
    except (IndexError, ValueError):
        return None

def parsear_producto_desde_texto(texto: str):
    """
    Recibe algo como '3 - Adidas | Pure Game (masculino)' y devuelve 'Adidas | Pure Game (masculino)'.
    """
    try:
        return texto.split(" - ", 1)[1]
    except IndexError:
        return texto