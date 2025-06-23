from scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class MercadoLibreScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.mercadolibre.com.co")
        
    def search_vehicles(self, search_term, max_pages=1):
        search_url = f"{self.base_url}/cars-trucks/_Tienda_mercado-libre#applied_filter_id%3Dcategory%26applied_filter_name%3DCategor%C3%ADas%26applied_filter_order%3D2%26applied_value_id%3DMCO1744%26applied_value_name%3DAutomotriz%26applied_value_order%3D2%26applied_value_results%3D7%26is_custom%3Dfalse"
        
        self.driver.get(search_url)
        time.sleep(3)  # Esperar a que cargue la página
        
        # Aceptar cookies si aparece el banner
        try:
            cookie_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Entendido")]')
            cookie_button.click()
            time.sleep(1)
        except:
            pass
        
        # Realizar la búsqueda
        try:
            search_box = self.driver.find_element(By.NAME, "as_word")
            search_box.clear()
            search_box.send_keys(search_term)
            search_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            search_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error al realizar la búsqueda: {e}")
            return []
        
        vehicles = []
        current_page = 1
        
        while current_page <= max_pages:
            print(f"Extrayendo datos de la página {current_page}...")
            
            # Obtener HTML de la página actual
            html = self.driver.page_source
            page_vehicles = self.parse_vehicle_list(html)
            vehicles.extend(page_vehicles)
            
            # Intentar ir a la siguiente página
            if current_page < max_pages:
                try:
                    next_button = self.driver.find_element(By.XPATH, '//a[contains(@title, "Siguiente")]')
                    next_button.click()
                    time.sleep(3)  # Esperar a que cargue la nueva página
                    current_page += 1
                except:
                    print("No se encontró el botón de siguiente página.")
                    break
        
        return vehicles
    
    def parse_vehicle_list(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        vehicle_items = soup.find_all('li', class_='ui-search-layout__item')
        
        vehicles = []
        
        for item in vehicle_items:
            try:
                vehicle = {}
                
                # Información básica
                title = item.find('h2', class_='ui-search-item__title').text.strip()
                vehicle['title'] = title
                
                # Extraer marca y modelo del título (puede necesitar ajustes)
                brand_model = title.split(' ')
                vehicle['brand'] = brand_model[0] if len(brand_model) > 0 else ''
                vehicle['model'] = ' '.join(brand_model[1:3]) if len(brand_model) > 1 else ''
                
                # Precio
                price_str = item.find('span', class_='price-tag-fraction').text.strip()
                price_str = price_str.replace('.', '')  # Eliminar puntos de separación de miles
                vehicle['price'] = float(price_str)
                vehicle['currency'] = 'COP'  # Asumimos pesos colombianos
                
                # Año (extraído del título o de atributos específicos)
                year_match = re.search(r'\b(19|20)\d{2}\b', title)
                vehicle['year'] = int(year_match.group(0)) if year_match else None
                
                # Imagen
                image = item.find('img', class_='ui-search-result-image__element')
                vehicle['image_url'] = image['data-src'] if image and 'data-src' in image.attrs else image['src'] if image else None
                
                # URL del vehículo
                link = item.find('a', class_='ui-search-link')['href']
                vehicle['url'] = link
                
                # Fuente
                vehicle['source'] = 'Mercado Libre'
                
                # Intentar obtener más detalles de la página del vehículo
                try:
                    details = self.parse_vehicle_details(link)
                    vehicle.update(details)
                except Exception as e:
                    print(f"Error al obtener detalles adicionales: {e}")
                
                vehicles.append(vehicle)
                
            except Exception as e:
                print(f"Error al procesar un vehículo: {e}")
                continue
        
        return vehicles
    
    def parse_vehicle_details(self, vehicle_url):
        self.driver.get(vehicle_url)
        time.sleep(2)  # Esperar a que cargue la página
        
        details = {}
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ubicación
        try:
            location = soup.find('span', class_='ui-pdp-color--BLACK').text.strip()
            details['location'] = location
        except:
            pass
        
        # Atributos principales (kilometraje, transmisión, etc.)
        try:
            attributes = soup.find_all('tr', class_='andes-table__row')
            for attr in attributes:
                th = attr.find('th')
                td = attr.find('td')
                if th and td:
                    attr_name = th.text.strip().lower()
                    attr_value = td.text.strip()
                    
                    if 'kilómetros' in attr_name:
                        details['mileage'] = int(attr_value.replace('.', '').replace(' km', ''))
                    elif 'transmisión' in attr_name:
                        details['transmission'] = attr_value
                    elif 'motor' in attr_name:
                        details['engine'] = attr_value
                    elif 'combustible' in attr_name:
                        details['fuel_type'] = attr_value
        except Exception as e:
            print(f"Error al extraer atributos: {e}")
        
        return details