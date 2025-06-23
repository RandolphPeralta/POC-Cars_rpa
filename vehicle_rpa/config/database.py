from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración alternativa que evita problemas con caracteres especiales
DB_CONFIG = {
    'username': 'root',
    'password': 'yokona@76',  # La contraseña con @ se pasa como parámetro separado
    'host': 'localhost',
    'port': '3306',
    'database': 'vehicle_db'
}

# Construye la cadena de conexión sin incluir la contraseña directamente en la URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_CONFIG['username']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(DATABASE_URL, connect_args={'password': DB_CONFIG['password']})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()