FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias primero (aprovecha la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

EXPOSE 5000

CMD ["python", "-m", "app.main"]
