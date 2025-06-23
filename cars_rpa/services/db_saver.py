from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from urllib.parse import quote_plus
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definición de la base declarativa para SQLAlchemy
Base = declarative_base()

class Carro(Base):
    """Modelo ORM para la tabla carros"""
    __tablename__ = 'carros'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    precio = Column(String(50))
    año = Column(String(20))
    kilometraje = Column(String(50))
    ubicacion = Column(String(100))
    fecha_creacion = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    
    # Definición de la restricción única
    __table_args__ = (
        UniqueConstraint('titulo', 'precio', 'año', name='unique_carro'),
    )

def get_db_session():
    """Crea y retorna una sesión de base de datos"""
    try:
        # Codificar la contraseña para manejar caracteres especiales
        password = "Yokona@76"
        encoded_password = quote_plus(password)
        
        # Configuración de la conexión
        engine = create_engine(
            f'mysql+mysqlconnector://root:{encoded_password}@localhost/vehicle_db',
            echo=False,
            pool_pre_ping=True
        )
        
        # Crear las tablas si no existen
        Base.metadata.create_all(engine)
        
        # Crear fábrica de sesiones
        Session = sessionmaker(bind=engine)
        return Session()
        
    except SQLAlchemyError as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise

def save_carros_to_db(carros):
    """Guarda los carros en la base de datos con mejor registro de estadísticas"""
    if not carros:
        logger.warning("No hay carros para guardar.")
        return

    session = None
    stats = {
        'total': len(carros),
        'nuevos': 0,
        'actualizados': 0,
        'duplicados': 0,
        'errores': 0
    }
    
    try:
        session = get_db_session()
        
        for carro_data in carros:
            try:
                precio_numero = ''.join(c for c in carro_data['precio'] if c.isdigit())
                
                # Verificar si el carro ya existe
                exists = session.query(Carro).filter_by(
                    titulo=carro_data['titulo'],
                    precio=precio_numero,
                    año=carro_data['año']
                ).first()
                
                if exists:
                    # Actualizar solo si hay cambios
                    if (exists.kilometraje != carro_data['kilometraje'] or 
                        exists.ubicacion != carro_data['ubicacion']):
                        exists.kilometraje = carro_data['kilometraje']
                        exists.ubicacion = carro_data['ubicacion']
                        stats['actualizados'] += 1
                    else:
                        stats['duplicados'] += 1
                else:
                    # Crear nuevo registro
                    carro = Carro(
                        titulo=carro_data['titulo'],
                        precio=precio_numero,
                        año=carro_data['año'],
                        kilometraje=carro_data['kilometraje'],
                        ubicacion=carro_data['ubicacion']
                    )
                    session.add(carro)
                    stats['nuevos'] += 1
                
                session.commit()
                
            except IntegrityError:
                session.rollback()
                stats['duplicados'] += 1
                logger.debug(f"Registro duplicado: {carro_data.get('titulo')}")
            except Exception as e:
                session.rollback()
                stats['errores'] += 1
                logger.error(f"Error procesando carro {carro_data.get('titulo')}: {e}")
        
        # Reporte detallado
        logger.info("\n📊 Estadísticas de Guardado:")
        logger.info(f"  - Total procesados: {stats['total']}")
        logger.info(f"  - Nuevos registros: {stats['nuevos']}")
        logger.info(f"  - Registros actualizados: {stats['actualizados']}")
        logger.info(f"  - Registros sin cambios: {stats['duplicados']}")
        logger.info(f"  - Errores: {stats['errores']}")
        
    except SQLAlchemyError as e:
        if session:
            session.rollback()
        logger.error(f"Error en la transacción de base de datos: {e}")
        raise
    finally:
        if session:
            session.close()