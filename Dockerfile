# Utiliza una imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt /app/
COPY . /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Crea las carpetas necesarias para archivos estáticos y de medios
RUN mkdir -p /app/staticfiles /app/media

# Exponer el puerto 8000 para el servidor
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
