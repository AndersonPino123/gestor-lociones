# views/graficos.py

import pandas as pd
import streamlit as st
from database.connection import obtener_conexion_cursor


def mostrar_grafico_lineas():
    st.title("📈 Gráfico de Ventas por Fecha")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            """
            SELECT fecha, SUM(valor) AS total
            FROM compras
            GROUP BY fecha
            ORDER BY fecha;
        """
        )
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


def mostrar_grafico_barras():
    st.title("📊 Total de compras por cliente")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            """
            SELECT c.nombre, COUNT(co.id) 
            FROM clientes c
            JOIN compras co ON c.id = co.cliente_id
            GROUP BY c.nombre
            ORDER BY COUNT(co.id) DESC
        """
        )
        datos = cursor.fetchall()
        conexion.close()

        if datos:
            df = pd.DataFrame(datos, columns=["Cliente", "Compras"])
            st.bar_chart(df.set_index("Cliente"))
        else:
            st.info("No hay datos de compras para graficar.")
    except Exception as e:
        st.error(f"❌ Error al generar el gráfico de barras: {e}")


def mostrar_grafico_torta():
    st.title("🍰 Porcentaje de gasto por cliente")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute(
            """
            SELECT c.nombre, SUM(co.valor)
            FROM clientes c
            JOIN compras co ON c.id = co.cliente_id
            GROUP BY c.nombre
            ORDER BY SUM(co.valor) DESC;
        """
        )
        datos = cursor.fetchall()
        conexion.close()

        if datos:
            df = pd.DataFrame(datos, columns=["Cliente", "Gasto"])
            st.plotly_chart(
                st.plotly_pie_chart(
                    df, names="Cliente", values="Gasto", title="Distribución de gasto"
                )
            )
        else:
            st.info("No hay datos de gasto para graficar.")
    except Exception as e:
        st.error(f"❌ Error al generar el gráfico de torta: {e}")
