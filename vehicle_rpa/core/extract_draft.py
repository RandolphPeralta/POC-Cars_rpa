import json
import requests
from bs4 import BeautifulSoup as bs

url = "https://carros.mercadolibre.com.co/usados/"

# Paso 1: Obtener el contenido HTML
html = requests.get(url)
content = html.content
soup = bs(content, "lxml")

# Paso 2: Buscar el <script> con los datos JSON
script_data = None
for script in soup.find_all("script"):
    if "results" in script.text and "polycard" in script.text:
        script_data = script.text
        break

# Paso 3: Limpiar y convertir a dict
json_text = script_data.strip()
start = json_text.find('{')
end = json_text.rfind('}') + 1
json_data = json.loads(json_text[start:end])

# Paso 4: Extraer la información de los autos
autos = []

# Función recursiva para buscar 'polycard' en el JSON
def find_polycards(data):
    if isinstance(data, dict):
        if 'polycard' in data and isinstance(data['polycard'], dict):
            # Verificar si es un polycard de auto (contiene 'components' con 'title' y 'price')
            if 'components' in data['polycard']:
                components = data['polycard']['components']
                titulo = None
                precio = None
                for component in components:
                    if component.get('type') == 'title':
                        titulo = component.get('title', {}).get('text', 'Sin título')
                    elif component.get('type') == 'price':
                        precio = component.get('price', {}).get('current_price', {}).get('value', 0)
                if titulo and precio:
                    autos.append({'titulo': titulo, 'precio': precio})
        # Buscar en los valores del diccionario
        for key in data:
            find_polycards(data[key])
    elif isinstance(data, list):
        # Buscar en los elementos de la lista
        for item in data:
            find_polycards(item)

# Buscar polycards en todo el JSON
find_polycards(json_data)

# Mostrar los resultados
for auto in autos:
    print(f"Auto: {auto['titulo']}")
    print(f"Precio: ${auto['precio']:,.0f} COP")
    print("-" * 50)

# Opcional: Guardar en un DataFrame (pandas) o CSV
import pandas as pd
if autos:
    df = pd.DataFrame(autos)
    print("\nDataFrame con los resultados:")
    print(df)
    # df.to_csv('autos_mercadolibre.csv', index=False)  # Descomenta para guardar en CSV
else:
    print("No se encontraron autos en el JSON.")