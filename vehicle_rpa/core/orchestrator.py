from core.extract import get_autos
from services.bq_saver import save_autos_to_db

def run_pipeline():
    print("Extrayendo datos...")
    autos = get_autos()
    print(f"{len(autos)} autos extraídos.")
    print("Guardando en base de datos...")
    save_autos_to_db(autos)