# Usar imagen oficial ligera de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requerimientos e instalarlos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y las pruebas
COPY src/ ./src/
COPY tests.py ./

# Comando por defecto al ejecutar el contenedor
CMD ["pytest", "tests.py"]
