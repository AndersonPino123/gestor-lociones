# views/catalogo_view.py

import streamlit as st
from modules.productos import obtener_catalogo

def mostrar_catalogo():
    st.title("🛍️ Catálogo de Lociones")
    
    filtro_genero = st.sidebar.selectbox("Filtrar por género", ["Todos", "Femenino", "Masculino"])
    productos = obtener_catalogo(filtro_genero)

    if productos:
        for marca, nombre, fragancia, cantidad, precio, imagen_url in productos:
            with st.container():
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(imagen_url or "https://via.placeholder.com/120", width=120)
                with cols[1]:
                    st.markdown(f"#### 🏷️ Marca: {marca}")
                    st.markdown(f"### {nombre}")
                    st.markdown(f"- 🌸 Fragancia: {fragancia}")
                    st.markdown(f"- 🧪 Cantidad: {cantidad} ml")
                    st.markdown(f"- 💰 Precio: ${precio:,.0f}")
                    st.markdown("---")
    else:
        st.info("No hay productos disponibles para mostrar.")