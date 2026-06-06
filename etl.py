import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root1234',
    database='dhl_dw'
)
cursor = conn.cursor()

# Cargar dimensiones
cursor.execute("INSERT INTO dim_cliente SELECT id_cliente, nombre, sector, ciudad FROM clientes")
cursor.execute("INSERT INTO dim_producto SELECT id_producto, nombre, categoria, requiere_frio FROM productos")
cursor.execute("INSERT INTO dim_empleado SELECT id_empleado, nombre, puesto, almacen FROM empleados")

# Cargar dim_tiempo con fechas únicas
cursor.execute("SELECT DISTINCT fecha FROM ventas")
fechas = cursor.fetchall()
meses = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
         7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
for i, (fecha,) in enumerate(fechas, 1):
    cursor.execute(
        "INSERT INTO dim_tiempo VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (i, fecha, fecha.day, fecha.month,
         (fecha.month-1)//3+1, fecha.year, meses[fecha.month])
    )

conn.commit()

# Cargar fact_ventas
cursor.execute("""
    INSERT INTO fact_ventas (id_cliente, id_producto, id_empleado, id_tiempo, cantidad, costo_unitario, total, almacen)
    SELECT v.id_cliente, v.id_producto, v.id_empleado, t.id_tiempo,
           v.cantidad, v.costo_unitario, v.total, v.almacen
    FROM ventas v
    JOIN dim_tiempo t ON v.fecha = t.fecha
""")

conn.commit()
cursor.close()
conn.close()
print("✅ ETL completado correctamente")