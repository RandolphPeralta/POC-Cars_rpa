# 🚗 cars_rpa

Proyecto de automatización de scraping de información de vehículos usando Selenium, Docker y MySQL.

## 📦 Descripción

Este proyecto extrae datos de vehículos desde un portal web mediante Selenium, guarda la información en una base de datos MySQL, y está completamente dockerizado para facilitar su despliegue y ejecución.

## 🧱 Estructura del Proyecto

```plaintext
cars_rpa/
├── core/
│ ├── extract.py # Módulo de scraping con Selenium
│ ├── db.py # Conexión y operaciones con MySQL
│ └── orchestrator.py # Controlador principal del pipeline
├── requirements.txt # Dependencias de Python
├── Dockerfile # Imagen del scraper
├── docker-compose.yml # Orquestación de servicios
└── README.md # Documentación del proyecto
```

## 🐳 Docker

### 🛠 Requisitos previos

- Docker instalado: https://docs.docker.com/get-docker/
- Docker Compose

### ▶️ Ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/RandolphPeralta/cars_rpa.git
cd cars_rpa
```

2. Construye y levanta los contenedores:

- docker-compose up --build

Esto levantará dos servicios:

car_mysql: Base de datos MySQL.

car_scraper: Contenedor de scraping con Selenium.

Nota: el primer inicio descargará chromedriver y puede tomar tiempo. Asegúrate de que la versión de Chrome y chromedriver sean compatibles.

## 🚀 Cómo Ejecutar
1. Instalar dependencias y preparar el entorno virtual:

```bash
# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv

source venv/bin/activate  # En Linux/Mac

venv\Scripts\activate  # En Windows

pip install --upgrade pip

pip install -r requirements.txt

# Desactivar el entorno virtual cuando termines
deactivate

```

2. Ejecutar el procesamiento:

```bash
# Asegúrate de tener las credenciales de Google Cloud configuradas
python main.py
```