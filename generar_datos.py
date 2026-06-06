import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

fake = Faker('es_MX')

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root1234',
    database='dhl_dw'
)
cursor = conn.cursor()

# Clientes
sectores = ['Farmacéutico', 'Retail', 'Consumo Masivo', 'Automotriz', 'Tecnología']
ciudades = ['CDMX', 'Guadalajara', 'Monterrey', 'Puebla', 'Querétaro']
for _ in range(50):
    cursor.execute("INSERT INTO clientes (nombre, sector, ciudad, fecha_registro) VALUES (%s,%s,%s,%s)",
        (fake.company(), random.choice(sectores), random.choice(ciudades), fake.date_between('-2y','today')))

# Productos
categorias = ['Medicamentos', 'Ropa', 'Alimentos', 'Electrónicos', 'Refacciones']
for _ in range(30):
    cursor.execute("INSERT INTO productos (nombre, categoria, peso_kg, requiere_frio) VALUES (%s,%s,%s,%s)",
        (fake.word().capitalize(), random.choice(categorias), round(random.uniform(0.5,50),2), random.choice([0,1])))

# Empleados
puestos = ['Operador', 'Supervisor', 'Chofer', 'Analista']
almacenes = ['CDMX Norte', 'CDMX Sur', 'Guadalajara', 'Monterrey']
for _ in range(20):
    cursor.execute("INSERT INTO empleados (nombre, puesto, almacen, fecha_ingreso) VALUES (%s,%s,%s,%s)",
        (fake.name(), random.choice(puestos), random.choice(almacenes), fake.date_between('-5y','today')))

conn.commit()

# Ventas - 6000 registros
fecha_inicio = date(2024, 12, 1)
for _ in range(6000):
    fecha = fecha_inicio + timedelta(days=random.randint(0, 180))
    cantidad = random.randint(1, 100)
    costo = round(random.uniform(50, 5000), 2)
    cursor.execute("INSERT INTO ventas (id_cliente, id_producto, id_empleado, fecha, cantidad, costo_unitario, total, almacen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
        (random.randint(1,50), random.randint(1,30), random.randint(1,20),
         fecha, cantidad, costo, round(cantidad*costo,2), random.choice(almacenes)))

conn.commit()
cursor.close()
conn.close()
print("✅ Datos generados correctamente")