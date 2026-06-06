import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="DHL Supply Chain — Dashboard", layout="wide")
st.title("🚚 DHL Supply Chain México — Dashboard de Análisis")
st.markdown("Sistema de Soporte a la Toma de Decisiones (DSS)")

conn = mysql.connector.connect(
    host='127.0.0.1', user='root',
    password='root1234', database='dhl_dw'
)

df = pd.read_sql("""
    SELECT f.total, f.cantidad, f.almacen,
           c.sector, c.ciudad, c.nombre as cliente,
           p.categoria, p.nombre as producto,
           t.mes, t.nombre_mes, t.anio
    FROM fact_ventas f
    JOIN dim_cliente c ON f.id_cliente = c.id_cliente
    JOIN dim_producto p ON f.id_producto = p.id_producto
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
""", conn)

# Filtros
st.sidebar.header("Filtros")
sector = st.sidebar.multiselect("Sector", df['sector'].unique(), default=df['sector'].unique())
almacen = st.sidebar.multiselect("Almacén", df['almacen'].unique(), default=df['almacen'].unique())
df_f = df[df['sector'].isin(sector) & df['almacen'].isin(almacen)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas Totales", f"${df_f['total'].sum():,.0f}")
col2.metric("📦 Total Pedidos", f"{len(df_f):,}")
col3.metric("📊 Ticket Promedio", f"${df_f['total'].mean():,.0f}")

st.divider()

# Gráfica 1
col1, col2 = st.columns(2)
with col1:
    st.subheader("Ventas por Mes")
    fig, ax = plt.subplots()
    ventas_mes = df_f.groupby('nombre_mes')['total'].sum().sort_values(ascending=False)
    sns.barplot(x=ventas_mes.index, y=ventas_mes.values, palette='Blues_d', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Ventas por Sector")
    fig2, ax2 = plt.subplots()
    ventas_sector = df_f.groupby('sector')['total'].sum().sort_values(ascending=False)
    sns.barplot(x=ventas_sector.index, y=ventas_sector.values, palette='Oranges_d', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Gráfica 3
st.subheader("Ventas por Almacén")
fig3, ax3 = plt.subplots()
ventas_almacen = df_f.groupby('almacen')['total'].sum().sort_values(ascending=False)
sns.barplot(x=ventas_almacen.index, y=ventas_almacen.values, palette='Greens_d', ax=ax3)
st.pyplot(fig3)

conn.close()