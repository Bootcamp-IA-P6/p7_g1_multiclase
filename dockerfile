FROM python:3.11-slim

# Evitamos que Python genere archivos basura (.pyc) y forzamos a que los logs salgan directo a consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema por si alguna librería compila en C (muy común en machine learning)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los archivos que definen las dependencias
COPY pyproject.toml ./
# Si usas uv, copiamos también el uv.lock. Si no, no molesta.
COPY uv.lock* ./

# Instalamos las dependencias. 
RUN pip install --no-cache-dir .

# Copiamos todo el resto del código de tu proyecto al contenedor
COPY . .

# Exponemos el puerto que usa Streamlit por defecto
EXPOSE 8501

# El comando que ejecutará el contenedor al encenderse
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]