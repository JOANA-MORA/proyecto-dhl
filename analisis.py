import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

conn = mysql.connector.connect(
    host='127.0.0.1', user='root',
    password='root1234', database='dhl_dw'
)

# Cargar datos del DW
df = pd.read_sql("""
    SELECT f.total, f.cantidad, f.almacen,
           c.sector, c.ciudad,
           p.categoria, t.mes, t.nombre_mes
    FROM fact_ventas f
    JOIN dim_cliente c ON f.id_cliente = c.id_cliente
    JOIN dim_producto p ON f.id_producto = p.id_producto
    JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
""", conn)

# Gráfica 1 - Ventas por mes
plt.figure(figsize=(10,5))
ventas_mes = df.groupby('nombre_mes')['total'].sum().sort_values(ascending=False)
sns.barplot(x=ventas_mes.index, y=ventas_mes.values, palette='Blues_d')
plt.title('Ventas Totales por Mes — DHL Supply Chain')
plt.xlabel('Mes')
plt.ylabel('Total ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ventas_por_mes.png')
plt.close()

# Gráfica 2 - Ventas por sector
plt.figure(figsize=(8,5))
ventas_sector = df.groupby('sector')['total'].sum().sort_values(ascending=False)
sns.barplot(x=ventas_sector.index, y=ventas_sector.values, palette='Oranges_d')
plt.title('Ventas por Sector de Cliente')
plt.xlabel('Sector')
plt.ylabel('Total ($)')
plt.tight_layout()
plt.savefig('ventas_por_sector.png')
plt.close()

# Clustering K-Means - Segmentación de clientes
clientes_df = pd.read_sql("""
    SELECT f.id_cliente,
           SUM(f.total) as total_compras,
           COUNT(*) as num_pedidos,
           AVG(f.cantidad) as promedio_cantidad
    FROM fact_ventas f
    GROUP BY f.id_cliente
""", conn)

scaler = StandardScaler()
X = scaler.fit_transform(clientes_df[['total_compras','num_pedidos','promedio_cantidad']])
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clientes_df['segmento'] = kmeans.fit_predict(X)

plt.figure(figsize=(8,5))
sns.scatterplot(data=clientes_df, x='total_compras', y='num_pedidos',
                hue='segmento', palette='Set1', s=100)
plt.title('Segmentación de Clientes — K-Means')
plt.xlabel('Total Compras ($)')
plt.ylabel('Número de Pedidos')
plt.tight_layout()
plt.savefig('clustering_clientes.png')
plt.close()

conn.close()
print("✅ Análisis completado — 3 gráficas generadas")