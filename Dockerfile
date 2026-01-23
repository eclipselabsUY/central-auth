# Base local para desarrollo
FROM python:3.12-alpine

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema necesarias
RUN apk update && apk add --no-cache \
    bash \
    libmagic \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    curl

# Instalar uv
RUN python -m ensurepip && python -m pip install --upgrade pip
RUN python -m pip install uv

# Crear directorio de trabajo
WORKDIR /app

# Copiar pyproject.toml para instalar dependencias
COPY pyproject.toml .
RUN uv sync

# Copiar el resto del código
COPY ./ ./app/

# Exponer puerto para Uvicorn
EXPOSE 8000

# Comando por defecto para desarrollo
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
