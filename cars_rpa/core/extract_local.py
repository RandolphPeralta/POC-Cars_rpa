from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import time
import os

def get_safe_text(element, selector, default="N/A"):
    """Obtiene texto de forma segura con reintentos"""
    attempts = 0
    while attempts < 3:
        try:
            elem = element.find_element(By.CSS_SELECTOR, selector)
            return elem.text if elem.text else default
        except (StaleElementReferenceException, NoSuchElementException):
            attempts += 1
            time.sleep(0.5)
    return default

def get_safe_list(element, selector, default="N/A"):
    """Obtiene lista de textos de forma segura con manejo mejorado de errores"""
    attempts = 0
    while attempts < 3:
        try:
            elements = element.find_elements(By.CSS_SELECTOR, selector)
            if not elements:
                return [default]
            return [el.text for el in elements] if elements else [default]
        except (StaleElementReferenceException, NoSuchElementException):
            attempts += 1
            time.sleep(0.5)
    return [default]

def extract_carros():
    # Configuración de Chrome
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.93 Safari/537.36")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--start-maximized")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument('--log-level=3')
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        # Cierra cualquier instancia previa de chromedriver
        os.system('taskkill /f /im chromedriver.exe /t >nul 2>&1')
        
        # Usa la ruta directa al chromedriver que descargaste
        driver_path = r"C:\Users\Rando\Downloads\chromedriver-win64\chromedriver.exe"
        service = Service(executable_path=driver_path)
        
        driver = webdriver.Chrome(service=service, options=opts)
        
    except Exception as e:
        print(f"Error al iniciar ChromeDriver: {str(e)}")
        raise Exception(f"No se pudo iniciar ChromeDriver: {str(e)}")

    carros = []
    
    try:
        driver.get('https://carros.mercadolibre.com.co/usados/')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.poly-card__content'))
        )
        
        items = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, 'div.poly-card__content')
        )
        
        for i, item in enumerate(items, 1):
            try:
                # Re-find el elemento para evitar StaleElementReferenceException
                current_items = driver.find_elements(By.CSS_SELECTOR, 'div.poly-card__content')
                if i > len(current_items):
                    break
                    
                item = current_items[i-1]  # Usamos i-1 porque el índice comienza en 0
                
                # Manejo más robusto de los atributos
                atributos = get_safe_list(item, 'ul.poly-attributes-list li.poly-attributes-list__item')
                
                carros.append({
                    'titulo': get_safe_text(item, 'h3.poly-component__title-wrapper a.poly-component__title'),
                    'precio': get_safe_text(item, 'span.andes-money-amount__fraction'),
                    'año': atributos[0] if len(atributos) > 0 else "N/A",
                    'kilometraje': atributos[1] if len(atributos) > 1 else "N/A",
                    'ubicacion': get_safe_text(item, 'span.poly-component__location')
                })
                
            except Exception as e:
                print(f"⚠️ Error procesando carro {i}: {str(e)}")
                continue

    finally:
        if 'driver' in locals():
            driver.quit()
    
    return carros