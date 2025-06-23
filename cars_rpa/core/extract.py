import os
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def get_safe_text(element, selector, default="N/A"):
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
    attempts = 0
    while attempts < 3:
        try:
            elements = element.find_elements(By.CSS_SELECTOR, selector)
            if not elements:
                return [default]
            return [el.text for el in elements if el.text.strip()] or [default]
        except (StaleElementReferenceException, NoSuchElementException):
            attempts += 1
            time.sleep(0.5)
    return [default]

def extract_carros():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.93 Safari/537.36")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--start-maximized")
    opts.add_argument('--headless')
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument('--log-level=3')
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument('--disable-software-rasterizer')
    opts.add_argument('--disable-extensions')
    opts.add_argument('--disable-background-networking')
    opts.add_argument('--disable-sync')
    opts.add_argument('--metrics-recording-only')
    opts.add_argument('--mute-audio')
    opts.add_argument('--disable-default-apps')

    try:
        driver_path = ChromeDriverManager().install()

        # Validar que el path devuelto sea un ejecutable, no un archivo de texto
        if not os.access(driver_path, os.X_OK):
            dir_path = Path(driver_path).parent
            real_binary = next((f for f in dir_path.iterdir() if f.is_file() and os.access(f, os.X_OK)), None)
            if not real_binary:
                raise Exception(f"No se encontró un ejecutable válido en: {dir_path}")
            driver_path = str(real_binary)

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=opts)

    except Exception as e:
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
                current_items = driver.find_elements(By.CSS_SELECTOR, 'div.poly-card__content')
                if i > len(current_items):
                    break

                item = current_items[i - 1]
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
        driver.quit()

    return carros
