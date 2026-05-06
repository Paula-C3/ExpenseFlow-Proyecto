FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos
# Usamos la ruta relativa al contexto de la raíz del proyecto
COPY backend/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# --- EL CAMBIO CLAVE ---
# Copiamos la carpeta 'backend' HACIA una carpeta llamada 'backend' en el contenedor
COPY backend/ /app/backend/

# Configuramos el PYTHONPATH para que Python sepa que /app es la raíz de los módulos
ENV PYTHONPATH=/app
ENV PORT=10000

# Ejecución usando la ruta del módulo correcta
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT}"]