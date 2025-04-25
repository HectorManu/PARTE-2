# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY ./app/ /app/

# Variables de entorno por defecto
ENV DATABASE_URL=sqlite:///./products.db
ENV HOST=0.0.0.0
ENV PORT=8000

# Puerto que estará expuesto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["sh", "-c", "python main.py --host $HOST --port $PORT"]
