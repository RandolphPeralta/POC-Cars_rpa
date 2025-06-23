import json
import requests
from bs4 import BeautifulSoup as bs

def get_autos():
    url = "https://carros.mercadolibre.com.co/usados/"
    html = requests.get(url)
    content = html.content
    soup = bs(content, "lxml")

    script_data = None
    for script in soup.find_all("script"):
        if "results" in script.text and "polycard" in script.text:
            script_data = script.text
            break

    if not script_data:
        return []

    json_text = script_data.strip()
    start = json_text.find('{')
    end = json_text.rfind('}') + 1
    json_data = json.loads(json_text[start:end])

    autos = []

    def find_polycards(data):
        if isinstance(data, dict):
            if 'polycard' in data and isinstance(data['polycard'], dict):
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
            for key in data:
                find_polycards(data[key])
        elif isinstance(data, list):
            for item in data:
                find_polycards(item)

    find_polycards(json_data)
    return autos

