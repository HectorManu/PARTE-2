# Proyecto de Scraping Web y API REST

Un sistema completo de web scraping con FastAPI que extrae información de productos de sitios web y los expone a través de una API REST con capacidades de filtrado y gestión.

## Características

- 🔍 **Web scraping robusto** con BeautifulSoup que maneja errores y reintentos
- 💾 **Almacenamiento en base de datos SQL** con SQLAlchemy
- 🌐 **API REST completa** con FastAPI que incluye:
  - Filtros avanzados (precio, título, categoría, rating)
  - Paginación integrada
  - Documentación automática con Swagger UI
- 🚀 **Endpoint para iniciar scraping** desde la API
- 🗑️ **Gestión de datos** con capacidad para limpiar la base de datos
- 📊 **Estadísticas** de productos recopilados
- 🐳 **Dockerizado** para fácil despliegue local y en la nube
- ☁️ **Listo para Render.com** para despliegue rápido

## Estructura del Proyecto

```
scraping-api-project/
├── app/
│   ├── __init__.py       # Archivo vacío para marcar el directorio como paquete
│   ├── models.py         # Modelos de la base de datos y Pydantic
│   ├── database.py       # Configuración de la base de datos
│   ├── scraper.py        # Lógica del web scraping
│   ├── api.py            # Endpoints de la API
│   └── main.py           # Punto de entrada principal
├── requirements.txt      # Dependencias
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Configuración de Docker Compose
├── .env                  # Variables de entorno
└── README.md             # Documentación
```

## Requisitos previos

- Python 3.9+
- Docker y Docker Compose (opcional, para despliegue en contenedores)
- Git (para clonar el repositorio)

## Instalación y Ejecución Local

### Opción 1: Con Python directamente

1. **Clonar el repositorio:**
   ```bash
   git clone 
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python -m app.main
   ```

5. **Acceder a la API:**
   - Documentación: http://127.0.0.1:8000/docs
   - API: http://127.0.0.1:8000

### Opción 2: Con Docker

1. **Clonar el repositorio:**
   ```bash
   git clone 
   ```

2. **Construir y ejecutar con Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la API:**
   - Documentación: http://localhost:8001/docs
   - API: http://localhost:8001

## Configuración de Variables de Entorno

El proyecto utiliza variables de entorno para facilitar la configuración en diferentes entornos. Estas variables se pueden configurar en el archivo `.env` para desarrollo local o directamente en el entorno de producción.

### Variables disponibles

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a la base de datos | `sqlite:///./products.db` |
| `HOST` | Host donde se ejecutará la API | `127.0.0.1` |
| `PORT` | Puerto donde se ejecutará la API | `8000` |

### Cuándo modificar las variables de entorno

Es necesario modificar estas variables en los siguientes casos:

1. **Cambio de base de datos**: 
   - Para usar PostgreSQL en lugar de SQLite:
     ```
     DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
     ```
   - Para usar MySQL:
     ```
     DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_db
     ```

2. **Cambio de puerto**:
   - Si el puerto 8000 está ocupado o deseas usar otro:
     ```
     PORT=8080
     ```
   - Recuerda también actualizar el `docker-compose.yml` si usas Docker:
     ```yaml
     ports:
       - "8080:8080"  # Externo:Interno
     ```

3. **Despliegue en producción**:
   - Para exponer la API públicamente:
     ```
     HOST=0.0.0.0
     ```
   - En Render.com, usa:
     ```
     PORT=10000
     ```

4. **Configuración de scraping automatizado**:
   - Para configurar la URL de scraping por defecto:
     ```
     DEFAULT_SCRAPE_URL=https://ejemplo.com
     ```
   - Para configurar el número de páginas por defecto:
     ```
     DEFAULT_SCRAPE_PAGES=10
     ```

### Cómo actualizar las variables de entorno

#### En desarrollo local

1. Crea o edita el archivo `.env` en la raíz del proyecto:
   ```bash
   nano .env
   ```

2. Añade o modifica las variables:
   ```
   DATABASE_URL=sqlite:///./products.db
   HOST=127.0.0.1
   PORT=8000
   ```

3. Guarda el archivo y reinicia la aplicación.

#### En Docker

1. Edita el archivo `docker-compose.yml`:
   ```yaml
   services:
     api:
       # ...
       environment:
         - DATABASE_URL=sqlite:///./products.db
         - HOST=0.0.0.0
         - PORT=8000
   ```

2. Reinicia los contenedores:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

#### En Render.com

1. En el dashboard de tu servicio, ve a la sección "Environment".
2. Añade o edita las variables necesarias.
3. Haz clic en "Save Changes" y espera a que el servicio se reinicie.

### Ejemplo de archivo .env completo

```
# Configuración de la base de datos
DATABASE_URL=sqlite:///./products.db

# Configuración del servidor
HOST=127.0.0.1
PORT=8000

# Configuración del scraper
DEFAULT_SCRAPE_URL=https://books.toscrape.com
DEFAULT_SCRAPE_PAGES=5

# Configuración de logging
LOG_LEVEL=INFO
```

Recuerda que el archivo `.env` debe estar incluido en tu `.gitignore` para evitar compartir credenciales sensibles en repositorios públicos.

## Uso de la API

Una vez que la aplicación está en ejecución, puedes usar la API de las siguientes formas:

### 1. Iniciar el proceso de scraping

Puedes iniciar el scraping directamente desde la API:

```bash
curl -X POST "http://localhost:8001/scrape/?url=https://books.toscrape.com&pages=5"
```

O desde la interfaz web de Swagger UI en `/docs`.

### 2. Consultar productos

Obtener todos los productos:
```bash
curl "http://localhost:8001/products/"
```

Con filtros:
```bash
curl "http://localhost:8001/products/?min_price=20&category=fiction&min_rating=4"
```

### 3. Eliminar todos los productos

Para borrar todos los productos y empezar de nuevo:
```bash
curl -X DELETE "http://localhost:8001/products/"
```

### 4. Ver estadísticas

Para obtener estadísticas de los productos recopilados:
```bash
curl "http://localhost:8001/stats/"
```

## Endpoints principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/products/` | Obtiene productos con filtros opcionales |
| GET | `/products/{id}` | Obtiene un producto específico por ID |
| POST | `/scrape/` | Inicia el scraping con parámetros personalizados |
| DELETE | `/products/` | Elimina todos los productos de la base de datos |
| GET | `/stats/` | Obtiene estadísticas sobre los productos recopilados |
| GET | `/categories/` | Obtiene todas las categorías disponibles |
| GET | `/health` | Health check (útil para monitoreo) |

## Parámetros de filtrado

En el endpoint `/products/` puedes utilizar los siguientes parámetros:

- `min_price`: Precio mínimo 
- `max_price`: Precio máximo
- `name`: Búsqueda por texto en el título
- `category`: Filtro por categoría exacta
- `min_rating`: Rating mínimo (0-5)
- `skip`: Para paginación, número de resultados a omitir
- `limit`: Número máximo de resultados a devolver

## Despliegue en Render.com

Para desplegar la aplicación en Render.com, sigue estos pasos:

1. **Sube tu código a un repositorio GitHub**

2. **Crea un nuevo Web Service en Render:**
   - Inicia sesión en [Render](https://render.com)
   - Haz clic en "New +"
   - Selecciona "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio con tu proyecto

3. **Configura el servicio:**
   - **Name**: Un nombre para tu servicio (ej. "scraping-api")
   - **Region**: Elige la región más cercana a tus usuarios
   - **Branch**: main (o master)
   - **Runtime**: Docker
   - **Instance Type**: Free (o el plan que necesites)

4. **Configura variables de entorno:**
   - `DATABASE_URL`: Para una base de datos persistente, usa PostgreSQL en Render
   - `HOST`: 0.0.0.0
   - `PORT`: 10000

5. **Health Check (opcional):**
   - **Path**: `/health`

6. **Crea el servicio:**
   - Haz clic en "Create Web Service"

7. **Ejecuta el scraper (opcional):**
   - Una vez que el servicio esté en funcionamiento, puedes usar el endpoint `/scrape/` o bien:
   - Ve a la pestaña "Shell" en el dashboard de Render
   - Ejecuta: `python -m app.main --scrape --url https://books.toscrape.com --pages 5`

8. **Accede a tu API:**
   - La URL será algo como `https://tu-servicio.onrender.com`
   - La documentación estará en `https://tu-servicio.onrender.com/docs`

## Personalización del scraper

Para adaptar el scraper a otro sitio web:

1. Modifica la función `parse_product_list` en `scraper.py`.
2. Ajusta los selectores CSS según la estructura de la página objetivo.
3. Si es necesario, modifica el modelo `ProductDB` para almacenar datos adicionales.

## Solución de problemas

### Error "address already in use"
Si obtienes un error de puerto en uso, modifica el puerto en `docker-compose.yml`:
```yaml
ports:
  - "8002:8000"  # Cambia 8001 por otro puerto disponible
```

### Problemas de codificación al extraer datos
El código ya maneja caracteres especiales como `Â` en precios, pero si encuentras otros problemas, revisa la función `parse_product_list` en `scraper.py`.

## Seguridad

### Protección del API

Por defecto, la API no implementa autenticación. Para entornos de producción, considera implementar uno de estos métodos:

1. **API Key**:
   - Añade un middleware que verifique una clave API en los headers:
   ```python
   from fastapi import FastAPI, Depends, HTTPException, Security, Header
   
   async def verify_api_key(x_api_key: str = Header(...)):
       if x_api_key != "tu_clave_secreta":
           raise HTTPException(status_code=403, detail="API Key inválida")
       return x_api_key
   
   @app.get("/products/", dependencies=[Depends(verify_api_key)])
   def get_products():
       # ...
   ```

2. **JWT (JSON Web Tokens)**:
   - Instala las dependencias: `pip install python-jose[cryptography] passlib[bcrypt]`
   - Implementa un sistema de autenticación basado en tokens

### Restricciones para scraping ético

Recuerda que el scraping debe ser ético y respetar los términos de servicio del sitio objetivo:

1. Añade delays suficientes entre peticiones (`time.sleep(random.uniform(1.0, 3.0))`)
2. Respeta el archivo robots.txt
3. Identifica tu scraper con un User-Agent honesto
4. No sobrecargues los servidores del sitio

Para implementar el respeto a robots.txt, añade esta función al scraper:

```python
from urllib.robotparser import RobotFileParser

def is_allowed(url: str, user_agent: str = "YourBot") -> bool:
    """Verifica si está permitido hacer scraping según robots.txt"""
    rp = RobotFileParser()
    parts = url.split("/")
    base_url = "/".join(parts[:3])
    rp.set_url(f"{base_url}/robots.txt")
    
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        logger.error(f"Error al verificar robots.txt: {e}")
        # En caso de error, permitimos por defecto pero con advertencia
        return True
```

## Solución de Problemas Adicionales

### Problemas comunes y soluciones

#### 1. Error al convertir tipos de datos

**Problema:** `Error: could not convert string to float: 'Â13.61'` u otros errores de conversión

**Solución:** 
- El código ya incluye manejo para el carácter `Â`, pero si encuentras otros caracteres problemáticos, actualiza la expresión regular en la función `parse_product_list`:
```python
clean_price = re.sub(r'[£€$Â\xa0\u202f\u00a0]', '', price_text)
```

#### 2. La base de datos no se actualiza correctamente

**Problema:** Los productos no se guardan o aparecen duplicados

**Solución:**
- Verifica permisos de escritura en el directorio de la base de datos
- Usa el endpoint DELETE `/products/` para limpiar la base antes de un nuevo scraping
- Revisa los logs para ver posibles errores durante el guardado

#### 3. El scraping no encuentra elementos en ciertas páginas

**Problema:** El scraper reporta 0 productos en algunas páginas mientras encuentra productos en otras

**Solución:**
- Verifica si la estructura HTML cambia entre páginas:
```python
# Añade esto al scraper para debug
soup_text = str(soup)[:1000]  # Primeros 1000 caracteres
logger.debug(f"Estructura HTML de la página: {soup_text}")
```
- Comprueba si hay paginación dinámica con JavaScript (puede requerir Selenium)

#### 4. Problemas con Docker

**Problema:** La aplicación no inicia correctamente en Docker

**Solución:**
- Verifica los logs: `docker-compose logs -f`
- Asegúrate de que los puertos no estén en uso: `netstat -tuln | grep 8001`
- Prueba con un puerto diferente en `docker-compose.yml`
- Asegúrate de que la configuración de base de datos es correcta para Docker

#### 5. Errores al desplegar en Render.com

**Problema:** La aplicación no se inicia o no responde en Render

**Solución:**
- Verifica que estás usando `HOST=0.0.0.0` y `PORT=10000` en la configuración
- Comprueba que los requisitos de la aplicación estén todos en `requirements.txt`
- Revisa los logs en el dashboard de Render para más detalles
- Si usas SQLite, asegúrate de que la carpeta tiene permisos de escritura

### Diagnóstico y Logging

Para un mejor diagnóstico, puedes aumentar el nivel de detalle de los logs:

1. En `logging.basicConfig()`, cambia el nivel:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Cambiar de INFO a DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

2. Para ver los detalles de las peticiones HTTP:
```python
# Añade esto cerca del inicio del archivo
import http.client as http_client
http_client.HTTPConnection.debuglevel = 1
```

3. Para registrar los logs en un archivo:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

## Mantenimiento y Escalabilidad

### Actualizaciones y Mantenimiento

#### Actualización de dependencias

Es importante mantener las dependencias actualizadas para evitar vulnerabilidades:

```bash
# Ver dependencias obsoletas
pip list --outdated

# Actualizar una dependencia específica
pip install --upgrade fastapi

# Actualizar todas las dependencias (con precaución)
pip install --upgrade -r requirements.txt

# Después de actualizar, regenera requirements.txt
pip freeze > requirements.txt
```

#### Adaptarse a cambios en sitios web

Los sitios web pueden cambiar su estructura HTML, lo que rompería el scraper. Estrategias para manejar esto:

1. **Monitoreo regular**: Configura verificaciones periódicas para confirmar que el scraper sigue funcionando
2. **Versionado de selectores**: Guarda la versión del sitio junto con los selectores utilizados
3. **Diseño adaptable**: Usa selectores CSS más generales cuando sea posible

Si el sitio cambia, actualiza la función `parse_product_list` para adaptarte a la nueva estructura.

### Escalabilidad

#### Procesamiento asíncrono

Para mejorar el rendimiento con grandes volúmenes de datos:

1. **Colas de tareas**: Implementa un sistema como Celery para procesar scraping en segundo plano:

```bash
pip install celery
```

```python
# tasks.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def run_scraping(url, pages):
    # Código de scraping aquí
    pass
```

2. **Scraping distribuido**: Para sitios muy grandes, considera dividir el trabajo entre varios workers:

```python
# En api.py
@app.post("/scrape-distributed/")
async def start_distributed_scraping(url: str, total_pages: int, workers: int = 3):
    pages_per_worker = total_pages // workers
    tasks = []
    
    for i in range(workers):
        start_page = i * pages_per_worker + 1
        end_page = (i + 1) * pages_per_worker if i < workers - 1 else total_pages
        tasks.append(run_scraping.delay(url, start_page, end_page))
    
    return {"status": "success", "message": f"Scraping distribuido iniciado con {workers} workers"}
```

#### Almacenamiento escalable

Para manejar grandes volúmenes de datos:

1. **Migrar a una base de datos más robusta**:
   - PostgreSQL para mayor rendimiento y soporte de búsqueda de texto completo
   - MongoDB para datos no estructurados o que cambian frecuentemente

2. **Implementar particionamiento**:
   - Divide los datos por fecha o categoría para mejorar el rendimiento de consultas

```python
# Ejemplo de configuración PostgreSQL con SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

#### Optimización de consultas

Para consultas más rápidas:

1. **Índices adicionales**:
```python
# En models.py
class ProductDB(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Ya indexado
    price = Column(Float, index=True)   # Añadir índice para búsquedas por precio
    # ...
```

2. **Caché de resultados frecuentes**:
```bash
pip install fastapi-cache2[redis]
```

```python
# En api.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/products/")
@cache(expire=60)  # Caché de 60 segundos
def get_products():
    # ...
```

### Monitoreo y Alertas

Para mantener el sistema funcionando correctamente:

1. **Logging centralizado**:
   - Usa servicios como ELK Stack (Elasticsearch, Logstash, Kibana) o Splunk
   - O implementa una solución simple con Papertrail o Loggly

2. **Métricas y dashboards**:
   - Prometheus + Grafana para monitoreo en tiempo real
   - Añade métricas personalizadas en puntos críticos:

```python
# Ejemplo de contador de productos scrapeados
from prometheus_client import Counter, start_http_server

PRODUCTS_SCRAPED = Counter('products_scraped_total', 'Total productos extraídos')

# En scraper.py
def save_products_to_db(self, products: List[Dict[str, Any]], db: Session) -> None:
    # ...código existente...
    PRODUCTS_SCRAPED.inc(len(products))  # Incrementa el contador
```

3. **Alertas automáticas**:
   - Configura alertas basadas en condiciones como:
     - Scraping con 0 productos encontrados
     - Tiempo de respuesta de API demasiado alto
     - Errores recurrentes

```python
# Ejemplo simplificado de sistema de alertas
def send_alert(message):
    # Enviar alerta por email, Slack, etc.
    pass

def check_scraping_health():
    if last_product_count == 0:
        send_alert("El último scraping no encontró productos")
```

Implementar estas prácticas te ayudará a mantener el sistema funcionando de manera fiable a largo plazo y a escalar a medida que crezcan tus necesidades.

## Consideraciones para producción

1. **Seguridad**: Añade autenticación a tu API (como JWT)
2. **Base de datos**: Cambia SQLite por PostgreSQL
3. **CORS**: Configura adecuadamente los dominios permitidos
4. **Rate limiting**: Añade limitaciones de tasa para prevenir abusos
5. **Monitoreo**: Implementa herramientas de monitoreo y alertas
6. **Backups**: Configura copias de seguridad de la base de datos
