# Etapa 1: construcción
FROM python:3.12-slim AS build

WORKDIR /app

# Copiar solo requirements si tuvieras, aquí es ejemplo mínimo
COPY app.py .

# Instalar dependencias si hubiera
# RUN pip install -r requirements.txt

# Etapa 2: producción
FROM python:3.12-slim

WORKDIR /app

# Crear usuario no root
RUN useradd -m appuser
USER appuser

# Copiar solo lo necesario desde la etapa de build
COPY --from=build /app/app.py .

# Variables de entorno
ENV MENSAJE="Hola desde Python optimizado en Docker!"

# Ejecutar app
CMD ["python", "app.py"]
