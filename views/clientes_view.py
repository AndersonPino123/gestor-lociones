# views/clientes_view.py

import streamlit as st
import pandas as pd
from modules.clientes import ver_clientes, agregar_cliente, actualizar_cliente, cambiar_estado_cliente

def mostrar_gestion_clientes():
    st.title("👥 Gestión de Clientes")

    # Mostrar tabla de clientes
    df = ver_clientes()
    st.dataframe(df, use_container_width=True)

    # Sección para agregar un nuevo cliente
    with st.expander("➕ Agregar nuevo cliente"):
        with st.form("form_nuevo_cliente"):
            nombre = st.text_input("Nombre")
            correo = st.text_input("Correo")
            edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
            submit = st.form_submit_button("Guardar")

            if submit:
                if nombre.strip() and correo.strip():
                    exito = agregar_cliente(nombre.strip(), correo.strip(), edad)
                    if exito:
                        st.success("✅ Cliente agregado con éxito. Recarga para ver reflejado.")
                else:
                    st.warning("⚠️ Nombre y correo son obligatorios.")

    st.markdown("---")
    st.subheader("✏️ Editar o cambiar estado de clientes")

    # Mostrar formulario para cada cliente
for _, fila in df.iterrows():
    with st.expander(f"👤 {fila['Nombre']} ({'Activo' if fila['Activo'] else 'Inactivo'})"):
        nuevo_nombre = st.text_input("Nombre", fila["Nombre"], key=f"nombre_{fila['ID']}")
        nuevo_correo = st.text_input("Correo", fila["Correo"], key=f"correo_{fila['ID']}")
        nueva_edad = st.number_input("Edad", value=fila["Edad"], min_value=0, max_value=120, step=1, key=f"edad_{fila['ID']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Guardar cambios", key=f"guardar_{fila['ID']}"):
                actualizado = actualizar_cliente(fila["ID"], nuevo_nombre, nuevo_correo, nueva_edad)
                if actualizado:
                    st.success("✅ Cambios guardados. Recarga para ver reflejado.")
        with col2:
            if fila["Activo"]:
                if st.button("🚫 Desactivar", key=f"desactivar_{fila['ID']}"):
                    cambiar_estado_cliente(fila["ID"], False)
                    st.warning("⚠️ Cliente desactivado. Recarga para ver reflejado.")
            else:
                if st.button("✅ Activar", key=f"activar_{fila['ID']}"):
                    cambiar_estado_cliente(fila["ID"], True)
                    st.success("✅ Cliente activado. Recarga para ver reflejado.")