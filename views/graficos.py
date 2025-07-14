# views/graficos.py

import pandas as pd
import streamlit as st
from database.connection import obtener_conexion_cursor

def mostrar_grafico_lineas():
    st.title("📈 Gráfico de Ventas por Fecha")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT fecha, SUM(valor) AS total
            FROM compras
            GROUP BY fecha
            ORDER BY fecha;
        """)
        datos = cursor.fetchall()
        conexion.close()

        if datos:
            df = pd.DataFrame(datos, columns=["Fecha", "Total"])
            df["Fecha"] = pd.to_datetime(df["Fecha"])
            st.line_chart(df.set_index("Fecha"))
        else:
            st.info("No hay datos de ventas para graficar.")
    except Exception as e:
        st.error(f"❌ Error al generar el gráfico: {e}")