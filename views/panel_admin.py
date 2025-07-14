# views/panel_admin.py

import pandas as pd
import streamlit as st
from database.connection import obtener_conexion_cursor

# --------- FUNCIONES DE REPORTES ---------

def mostrar_resumen_ventas():
    st.title("📊 Resumen de ventas del mes")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT SUM(valor) FROM compras
            WHERE DATE_PART('month', fecha) = DATE_PART('month', CURRENT_DATE)
            AND DATE_PART('year', fecha) = DATE_PART('year', CURRENT_DATE);
        """)
        total = cursor.fetchone()[0] or 0
        st.metric("💰 Total de ventas del mes", f"${total:,.0f}")
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al obtener el resumen: {e}")

def mostrar_compras_por_cliente():
    st.title("👥 Compras por Cliente")
    try:
        conexion, cursor = obtener_conexion_cursor()
        cursor.execute("""
            SELECT c.nombre, COUNT(co.id) AS cantidad, SUM(co.valor) AS total
            FROM clientes c
            JOIN compras co ON c.id = co.cliente_id
            GROUP BY c.nombre
            ORDER BY total DESC;
        """)
        resultados = cursor.fetchall()
        df = pd.DataFrame(resultados, columns=["Cliente", "Compras", "Total gastado"])
        st.dataframe(df, use_container_width=True)
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al consultar compras por cliente: {e}")

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
        df = pd.DataFrame(datos, columns=["Fecha", "Total"])
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        st.line_chart(df.set_index("Fecha"))
        conexion.close()
    except Exception as e:
        st.error(f"❌ Error al generar el gráfico: {e}")
