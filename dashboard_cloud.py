import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random
from datetime import date, timedelta

st.set_page_config(page_title="DHL Supply Chain — Dashboard", layout="wide")
st.title("🚚 DHL Supply Chain México — Dashboard de Análisis")
st.markdown("Sistema de Soporte a la Toma de Decisiones (DSS)")

# Generar datos simulados
random.seed(42)
sectores = ['Farmacéutico', 'Retail', 'Consumo Masivo', 'Automotriz', 'Tecnología']
almacenes = ['CDMX Norte', 'CDMX Sur', 'Guadalajara', 'Monterrey']
categorias = ['Medicamentos', 'Ropa', 'Alimentos', 'Electrónicos', 'Refacciones']
meses = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
         7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}

rows = []
fecha_inicio = date(2024, 12, 1)
for _ in range(6000):
    fecha = fecha_inicio + timedelta(days=random.randint(0, 180))
    cantidad = random.randint(1, 100)
    costo = round(random.uniform(50, 5000), 2)
    rows.append({
        'sector': random.choice(sectores),
        'almacen': random.choice(almacenes),
        'categoria': random.choice(categorias),
        'mes': fecha.month,
        'nombre_mes': meses[fecha.month],
        'cantidad': cantidad,
        'total': round(cantidad * costo, 2)
    })

df = pd.DataFrame(rows)

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

col1, col2 = st.columns(2)
with col1:
    st.subheader("Ventas por Mes")
    fig, ax = plt.subplots()
    v = df_f.groupby('nombre_mes')['total'].sum().sort_values(ascending=False)
    sns.barplot(x=v.index, y=v.values, palette='Blues_d', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Ventas por Sector")
    fig2, ax2 = plt.subplots()
    v2 = df_f.groupby('sector')['total'].sum().sort_values(ascending=False)
    sns.barplot(x=v2.index, y=v2.values, palette='Oranges_d', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

st.subheader("Ventas por Almacén")
fig3, ax3 = plt.subplots()
v3 = df_f.groupby('almacen')['total'].sum().sort_values(ascending=False)
sns.barplot(x=v3.index, y=v3.values, palette='Greens_d', ax=ax3)
st.pyplot(fig3)