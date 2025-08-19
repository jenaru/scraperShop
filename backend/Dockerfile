# Usa una imagen oficial de Python como base.
# Usar una versión específica es una buena práctica para la reproducibilidad.
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copia primero el archivo de dependencias.
# Esto aprovecha el cache de Docker: si requirements.txt no cambia,
# no se volverán a instalar las dependencias en cada build.
COPY requirements.txt requirements.txt

# Instala las dependencias del proyecto.
# --no-cache-dir reduce el tamaño de la imagen.
# --upgrade pip asegura que usamos la última versión de pip.
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo.
COPY ./app /app/app

# Expone el puerto 8000 para que el contenedor pueda recibir tráfico.
# Este es el puerto en el que Uvicorn correrá por defecto.
EXPOSE 8000

# Define el comando para ejecutar la aplicación cuando el contenedor se inicie.
# Uvicorn es un servidor ASGI de alto rendimiento.
# --host 0.0.0.0 hace que la aplicación sea accesible desde fuera del contenedor.
# --port 8000 coincide con el puerto expuesto.
# app.main:app se refiere al objeto 'app' de FastAPI dentro del archivo 'main.py' en el módulo 'app'.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
