# views/compras_view.py

import streamlit as st
from modules.clientes import obtener_clientes_activos
from modules.productos import obtener_productos_disponibles
from modules.compras import registrar_compra

def mostrar_registro_compra():
    st.title("🛒 Registrar nueva compra")

    # Obtener lista de clientes activos
    clientes = obtener_clientes_activos()
    if not clientes:
        st.warning("⚠️ No hay clientes activos disponibles.")
        return

    lista_clientes = [f"{id} - {nombre}" for id, nombre in clientes]
    seleccion_cliente = st.selectbox("Selecciona el cliente:", lista_clientes)
    cliente_id = int(seleccion_cliente.split(" - ")[0])

    # Obtener productos disponibles
    productos = obtener_productos_disponibles()
    if not productos:
        st.warning("⚠️ No hay productos disponibles.")
        return

    lista_productos = [f"{id} - {marca} | {nombre} ({genero.capitalize()})"
                       for id, marca, nombre, genero in productos]
    seleccion_producto = st.selectbox("Selecciona el producto comprado:", lista_productos)
    producto_nombre = seleccion_producto.split(" - ", 1)[1]  # Extrae la parte "Marca | Nombre (Género)"

    valor = st.number_input("Valor del producto", min_value=0.0, step=1000.0)

    if st.button("💾 Guardar compra"):
        if registrar_compra(cliente_id, producto_nombre, valor):
            st.success("✅ Compra registrada con éxito.")