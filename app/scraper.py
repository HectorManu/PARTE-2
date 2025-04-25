import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from models import ProductDB, Product

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')  # Eliminar posible barra al final
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """Obtiene una página con reintentos en caso de error"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Obteniendo página: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()  # Levanta excepciones para errores HTTP
                return BeautifulSoup(response.text, 'html.parser')
            except requests.exceptions.RequestException as e:
                logger.error(f"Error al obtener la página {url}: {e}")
                if attempt < max_retries - 1:
                    sleep_time = 2 ** attempt  # Backoff exponencial
                    logger.info(f"Reintentando en {sleep_time} segundos...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"No se pudo obtener la página después de {max_retries} intentos")
                    return None
    
    # Actualización para la función parse_product_list en scraper.py

    def parse_product_list(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extrae la lista de productos de una página
        
        Específicamente adaptado para books.toscrape.com
        """
        products = []
        
        # En books.toscrape.com, los productos están en elementos article con clase "product_pod"
        product_elements = soup.select('article.product_pod')
        logger.info(f"Encontrados {len(product_elements)} elementos de producto en la página")
        
        for element in product_elements:
            try:
                # Extraer datos del producto según la estructura de books.toscrape.com
                title_element = element.select_one('h3 a')
                price_element = element.select_one('div.product_price p.price_color')
                rating_element = element.select_one('p.star-rating')
                image_element = element.select_one('div.image_container img')
                
                # Verificar si encontramos los elementos básicos
                if not all([title_element, price_element]):
                    logger.warning("Producto incompleto, saltando...")
                    continue
                
                # Procesar y limpiar los datos
                # El título está en el atributo title del enlace
                title = title_element.get('title', '')
                
                # Depuramos para ver exactamente qué contiene el precio
                price_text = price_element.text.strip()
                logger.debug(f"Texto de precio original: '{price_text}'")
                
                # Convertir precio con manejo más robusto de caracteres especiales
                # Reemplazamos cualquier carácter no numérico excepto el punto decimal
                import re
                # Primero eliminamos el símbolo de libra y cualquier carácter no visible
                clean_price = re.sub(r'[£€$Â\s]', '', price_text)
                # Luego nos aseguramos de que solo queden números y punto decimal
                clean_price = re.sub(r'[^\d.]', '', clean_price)
                
                logger.debug(f"Precio limpio: '{clean_price}'")
                
                try:
                    price = float(clean_price)
                except ValueError:
                    logger.error(f"No se pudo convertir el precio '{price_text}' a float después de limpieza a '{clean_price}'")
                    # Establecemos un valor predeterminado para no perder el producto
                    price = 0.0
                
                # La categoría no está en la lista de productos, usamos "books" por defecto
                category = "books"
                
                # El rating está en la clase del elemento p.star-rating
                # Las clases son del tipo "star-rating Three", "star-rating Four", etc.
                rating_class = rating_element['class'] if rating_element and 'class' in rating_element.attrs else []
                rating_text = next((cls for cls in rating_class if cls != 'star-rating'), 'Zero')
                
                # Convertir rating de texto a número
                rating_map = {
                    'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
                }
                rating = rating_map.get(rating_text, 0)
                
                # Obtener URL de imagen si existe
                image_url = None
                if image_element and image_element.has_attr('src'):
                    # Las URLs de imágenes en books.toscrape.com son relativas
                    image_relative_url = image_element['src']
                    # Convertir a URL absoluta
                    if image_relative_url.startswith('/'):
                        image_url = f"{self.base_url}{image_relative_url}"
                    else:
                        # La URL es relativa a la ubicación actual
                        image_url = f"{self.base_url}/../{image_relative_url}"
                
                products.append({
                    "title": title,
                    "price": price,
                    "category": category,
                    "rating": rating,
                    "image_url": image_url
                })
                
                logger.info(f"Producto extraído: {title}, precio: {price}")
                
            except Exception as e:
                logger.error(f"Error al procesar un producto: {e}", exc_info=True)
                continue
        
        logger.info(f"Extraídos {len(products)} productos de {len(product_elements)} elementos")
        return products
    
    def scrape_products(self, num_pages: int = 5) -> List[Dict[str, Any]]:
        """Scrape de múltiples páginas de productos"""
        all_products = []
        
        # Basado en el HTML, vemos que la página principal muestra productos y tiene vínculos a páginas numeradas
        # Primera página
        first_page_url = self.base_url
        logger.info(f"Scraping página principal: {first_page_url}")
        
        soup = self.get_page(first_page_url)
        if soup:
            # Extraer productos
            page_products = self.parse_product_list(soup)
            logger.info(f"Encontrados {len(page_products)} productos en la página principal")
            all_products.extend(page_products)
            
            # Esperar entre solicitudes para ser respetuosos con el servidor
            time.sleep(random.uniform(1.0, 3.0))
        else:
            logger.error("No se pudo obtener la página principal")
            return all_products
        
        # Para el resto de páginas, miramos si hay enlaces de paginación
        # Como vemos en el HTML, los links están en formato "catalogue/page-2.html"
        for page in range(2, num_pages + 1):
            page_url = f"{self.base_url}/catalogue/page-{page}.html"
            logger.info(f"Scraping página {page}: {page_url}")
            
            soup = self.get_page(page_url)
            if not soup:
                logger.warning(f"No se pudo obtener la página {page}, continuando con la siguiente...")
                continue
            
            # Extraer productos
            page_products = self.parse_product_list(soup)
            logger.info(f"Encontrados {len(page_products)} productos en la página {page}")
            
            all_products.extend(page_products)
            
            # Esperar entre solicitudes para ser respetuosos con el servidor
            time.sleep(random.uniform(1.0, 3.0))
        
        return all_products
    
    def save_products_to_db(self, products: List[Dict[str, Any]], db: Session) -> None:
        """Guarda los productos en la base de datos"""
        for product_data in products:
            # Comprobar si el producto ya existe (por título)
            existing_product = db.query(ProductDB).filter(
                ProductDB.title == product_data["title"]
            ).first()
            
            if existing_product:
                # Actualizar producto existente
                for key, value in product_data.items():
                    setattr(existing_product, key, value)
                logger.info(f"Producto actualizado: {product_data['title']}")
            else:
                # Crear nuevo producto
                db_product = ProductDB(**product_data)
                db.add(db_product)
                logger.info(f"Nuevo producto añadido: {product_data['title']}")
        
        # Commit de los cambios
        db.commit()
        logger.info(f"Total de {len(products)} productos guardados en la base de datos")