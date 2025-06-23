import mysql.connector

def save_autos_to_db(autos):
    if not autos:
        print("No hay autos para guardar.")
        return

    conn = mysql.connector.connect(
        host="db", #localhost
        user="root",
        password="Yokona@76",
        database="vehicle_db"
    )

    cursor = conn.cursor()

    # Obtener títulos existentes
    cursor.execute("SELECT titulo FROM autos")
    existentes = set(titulo[0] for titulo in cursor.fetchall())

    nuevos_autos = [auto for auto in autos if auto['titulo'] not in existentes]

    for auto in nuevos_autos:
        cursor.execute(
            "INSERT INTO autos (titulo, precio) VALUES (%s, %s)",
            (auto['titulo'], auto['precio'])
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\nSe insertaron {len(nuevos_autos)} autos nuevos en la base de datos MySQL.")

