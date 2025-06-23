from core.extract import extract_carros
from services.db_saver import save_carros_to_db
import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('carros_pipeline.log'),
            logging.StreamHandler()
        ]
    )

def run_pipeline():
    configure_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Iniciando extracción de datos...")
        carros = extract_carros()
        logger.info(f"{len(carros)} carros extraídos correctamente.")
        
        logger.info("Iniciando guardado en base de datos...")
        save_carros_to_db(carros)
        logger.info("Proceso completado exitosamente.")
        
    except Exception as e:
        logger.error(f"Error en el pipeline: {str(e)}", exc_info=True)
        raise