# main.py
import logging
import argparse
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api import app as api_app
from database import engine
from models import Base
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Base de datos inicializada correctamente")
except SQLAlchemyError as e:
    logger.error(f"Error al inicializar la base de datos: {e}")
    raise

# Agregar CORS middleware
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    parser = argparse.ArgumentParser(description="Web Scraper y API de Productos")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "127.0.0.1"), 
                        help="Host para la API")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")), 
                        help="Puerto para la API")
    
    args = parser.parse_args()
    
    # Iniciar la API (el scraping ahora se maneja vía endpoints)
    logger.info(f"Iniciando API en {args.host}:{args.port}")
    
    # Usamos Application Factory de FastAPI para evitar problemas con múltiples instancias
    uvicorn.run(api_app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()