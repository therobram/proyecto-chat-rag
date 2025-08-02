FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para procesar PDFs
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

# Copiar y instalar dependencias primero (mejor cache)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copiar código fuente
COPY app/ ./app/
COPY scripts/ ./scripts/

# Crear directorios necesarios
RUN mkdir -p data vectorstore

# Hacer ejecutables los scripts
RUN chmod +x scripts/*.py

# Exponer puerto
EXPOSE 8000

# Script de inicio que limpia vectorstore si es necesario y ejecuta la app
CMD ["sh", "-c", "python scripts/init.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
