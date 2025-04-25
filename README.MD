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

## Consideraciones para producción

1. **Seguridad**: Añade autenticación a tu API (como JWT)
2. **Base de datos**: Cambia SQLite por PostgreSQL
3. **CORS**: Configura adecuadamente los dominios permitidos
4. **Rate limiting**: Añade limitaciones de tasa para prevenir abusos
5. **Monitoreo**: Implementa herramientas de monitoreo y alertas
6. **Backups**: Configura copias de seguridad de la base de datos