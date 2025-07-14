# views/lociones_view.py

import streamlit as st
import pandas as pd
from modules.productos import obtener_productos, agregar_locion

def mostrar_gestion_lociones():
    st.title("🧴 Lista de Lociones")
    
    # Mostrar lociones en tabla
    df = obtener_productos()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay lociones registradas.")

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
            exito = agregar_locion(marca, nombre_producto, ref_proveedor, genero, fragancia,
                                   cantidad, precio, stock, disponible, imagen_url)
            if exito:
                st.success("✅ Loción agregada con éxito.")
            else:
                st.error("❌ Ocurrió un error al guardar la loción.")