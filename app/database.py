import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener URL de base de datos desde variables de entorno o usar valor por defecto
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")

# Si la URL comienza con "postgres:" pero no tiene el prefijo "postgresql:",
# reemplazarlo (esto es común en Render y otros servicios en la nube)
if SQLALCHEMY_DATABASE_URL.startswith("postgres:"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres:", "postgresql:", 1)

try:
    # Configurar argumentos de conexión según el tipo de base de datos
    connect_args = {}
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args=connect_args
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
    # Caer de vuelta a SQLite si hay problemas
    fallback_url = "sqlite:///./products.db"
    print(f"Usando base de datos de respaldo: {fallback_url}")
    engine = create_engine(fallback_url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()