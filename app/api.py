from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models import Product, ProductCreate, ProductDB
from database import get_db, SessionLocal
from sqlalchemy import or_, and_
from scraper import WebScraper
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Product API",
    description="API para consultar productos extraídos mediante web scraping",
    version="1.0.0"
)

# Personalizar la documentación
@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Scraping API - Documentación",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
        swagger_favicon_url="/static/favicon.ico",
    )

# Añadir información de ayuda en la página de documentación
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scraping API - Documentación</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css" />
        <style>
            .banner {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
                border-left: 5px solid #007bff;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            .btn {
                display: inline-block;
                background-color: #007bff;
                color: white;
                padding: 10px 15px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 10px;
            }
            .btn:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="banner">
                <h2>Scraping API - Guía Rápida</h2>
                <p>Esta API te permite:</p>
                <ul>
                    <li><strong>Iniciar el scraping:</strong> Extrae productos de un sitio web y los guarda en la base de datos</li>
                    <li><strong>Buscar productos:</strong> Filtra productos por precio, nombre, categoría, etc.</li>
                    <li><strong>Eliminar productos:</strong> Borra todos los productos de la base de datos</li>
                    <li><strong>Ver estadísticas:</strong> Consulta estadísticas sobre los productos recopilados</li>
                </ul>
                <h3>Comenzar rápidamente:</h3>
                <ol>
                    <li>Inicia el scraping con <code>/scrape/</code> - Puedes especificar la URL y el número de páginas</li>
                    <li>Consulta los productos con <code>/products/</code> - Usa los parámetros para filtrar resultados</li>
                    <li>Si necesitas empezar de nuevo, usa <code>/products/</code> con método DELETE para limpiar la base de datos</li>
                </ol>
                <a href="/api/docs" class="btn">Ir a la documentación interactiva</a>
            </div>
            <div id="swagger-ui"></div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
        <script>
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                deepLinking: true
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Función para ejecutar el scraping en segundo plano
def run_scraping_task(url: str, pages: int):
    logger.info(f"Iniciando tarea de scraping de {url}, {pages} páginas")
    scraper = WebScraper(base_url=url)
    products = scraper.scrape_products(num_pages=pages)
    
    logger.info(f"Se encontraron {len(products)} productos en total")
    
    # Guardar en la base de datos
    with SessionLocal() as db:
        scraper.save_products_to_db(products, db)
    
    logger.info("Scraping completado y datos guardados en la base de datos")

# Endpoint de health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint para verificar que la API está funcionando correctamente.
    Utilizado por Render.com para health checks.
    """
    return {"status": "healthy"}

# Endpoint para iniciar el scraping
@app.post("/scrape/", tags=["Scraping"], summary="Iniciar scraping")
async def start_scraping(
    background_tasks: BackgroundTasks,
    url: str = Query("https://books.toscrape.com", description="URL base para el scraping"),
    pages: int = Query(5, description="Número de páginas a scrapear")
):
    """
    Inicia un proceso de scraping con los parámetros especificados.
    
    El scraping se ejecuta en segundo plano, por lo que este endpoint
    responde inmediatamente mientras el proceso continúa.
    
    - **url**: URL base del sitio web a scrapear (por defecto: books.toscrape.com)
    - **pages**: Número de páginas a scrapear (por defecto: 5)
    """
    # Añadir la tarea al procesamiento en segundo plano
    background_tasks.add_task(run_scraping_task, url, pages)
    
    return {
        "status": "success",
        "message": f"Proceso de scraping iniciado en segundo plano para {url}, {pages} páginas",
        "url": url,
        "pages": pages
    }

# Endpoint para eliminar todos los productos
@app.delete("/products/", tags=["Productos"], summary="Eliminar todos los productos")
def delete_all_products(db: Session = Depends(get_db)):
    """
    Elimina todos los productos de la base de datos.
    
    Este endpoint es útil para realizar pruebas o reiniciar el scraping.
    """
    try:
        # Eliminar todos los registros de la tabla de productos
        deleted_count = db.query(ProductDB).delete()
        db.commit()
        
        return {
            "status": "success",
            "message": f"Se han eliminado {deleted_count} productos de la base de datos"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar productos: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar productos: {str(e)}")


@app.get("/products/", response_model=List[Product], summary="Obtener productos con filtros")
def get_products(
    db: Session = Depends(get_db),
    min_price: Optional[float] = Query(None, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, description="Precio máximo"),
    name: Optional[str] = Query(None, description="Término de búsqueda para el título"),
    category: Optional[str] = Query(None, description="Categoría del producto"),
    min_rating: Optional[float] = Query(None, description="Rating mínimo"),
    skip: int = Query(0, description="Número de registros a omitir (paginación)"),
    limit: int = Query(100, description="Número máximo de registros a devolver")
):
    """
    Obtiene una lista de productos con filtros opcionales.
    
    - **min_price**: Filtra productos con precio mayor o igual al especificado
    - **max_price**: Filtra productos con precio menor o igual al especificado
    - **name**: Busca productos que contengan la cadena especificada en el título
    - **category**: Filtra productos por categoría exacta
    - **min_rating**: Filtra productos con rating mayor o igual al especificado
    - **skip**: Número de productos a omitir (para paginación)
    - **limit**: Número máximo de productos a devolver
    """
    query = db.query(ProductDB)
    
    # Aplicar filtros
    filters = []
    
    if min_price is not None:
        filters.append(ProductDB.price >= min_price)
    
    if max_price is not None:
        filters.append(ProductDB.price <= max_price)
    
    if name:
        filters.append(ProductDB.title.ilike(f"%{name}%"))
    
    if category:
        filters.append(ProductDB.category == category)
    
    if min_rating is not None:
        filters.append(ProductDB.rating >= min_rating)
    
    # Aplicar todos los filtros si existen
    if filters:
        query = query.filter(and_(*filters))
    
    # Aplicar paginación
    products = query.offset(skip).limit(limit).all()
    
    return products

@app.get("/products/{product_id}", response_model=Product, summary="Obtener un producto por ID")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto específico por su ID.
    
    - **product_id**: ID único del producto
    """
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@app.get("/categories/", response_model=List[str], summary="Obtener todas las categorías")
def get_categories(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todas las categorías disponibles.
    """
    # Obtener categorías únicas
    categories = db.query(ProductDB.category).distinct().all()
    return [category[0] for category in categories]

# Endpoint para obtener estadísticas
@app.get("/stats/", tags=["Estadísticas"], summary="Obtener estadísticas de productos")
def get_stats(db: Session = Depends(get_db)):
    """
    Obtiene estadísticas generales sobre los productos en la base de datos.
    
    Devuelve:
    - Total de productos
    - Precio promedio
    - Precio mínimo
    - Precio máximo
    - Distribución de ratings
    - Productos por categoría
    """
    # Total de productos
    total_products = db.query(ProductDB).count()
    
    # Si no hay productos, devolver estadísticas vacías
    if total_products == 0:
        return {
            "total_products": 0,
            "price_stats": {
                "average": 0,
                "min": 0,
                "max": 0
            },
            "rating_distribution": {},
            "categories": {}
        }
    
    # Estadísticas de precio
    from sqlalchemy import func
    price_stats = db.query(
        func.avg(ProductDB.price).label("average"),
        func.min(ProductDB.price).label("min"),
        func.max(ProductDB.price).label("max")
    ).one()
    
    # Distribución de ratings
    rating_counts = db.query(
        ProductDB.rating,
        func.count(ProductDB.id).label("count")
    ).group_by(ProductDB.rating).all()
    
    rating_distribution = {int(rating): count for rating, count in rating_counts}
    
    # Productos por categoría
    category_counts = db.query(
        ProductDB.category,
        func.count(ProductDB.id).label("count")
    ).group_by(ProductDB.category).all()
    
    categories = {category: count for category, count in category_counts}
    
    return {
        "total_products": total_products,
        "price_stats": {
            "average": float(price_stats.average) if price_stats.average else 0,
            "min": float(price_stats.min) if price_stats.min else 0,
            "max": float(price_stats.max) if price_stats.max else 0
        },
        "rating_distribution": rating_distribution,
        "categories": categories
    }