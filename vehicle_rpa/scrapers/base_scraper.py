from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.driver = self._setup_driver()
        
    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo sin cabeza
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Configuración para evitar detección como bot
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(executable_path='/usr/local/bin/chromedriver')  # Ajustar según tu sistema
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    def search_vehicles(self, search_term, max_pages=1):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas")
    
    def parse_vehicle_list(self, html):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas")
    
    def parse_vehicle_details(self, vehicle_url):
        raise NotImplementedError("Este método debe ser implementado por las clases hijas")
    
    def close(self):
        self.driver.quit()