import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host="localhost",
    user="root",        # ← Cambia esto
    password="Yokona@76", # ← Cambia esto
    database="vehicle_db"
)

cursor = conn.cursor()

# Insertar autos en la tabla
for auto in autos:
    cursor.execute(
        "INSERT INTO autos (titulo, precio) VALUES (%s, %s)",
        (auto['titulo'], auto['precio'])
    )

conn.commit()
cursor.close()
conn.close()

print(f"\nSe insertaron {len(autos)} autos en la base de datos MySQL.")
