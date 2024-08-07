
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Configurar la zona horaria
ENV TZ=America/Asuncion
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Copia el archivo de requisitos y los instala
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto en el directorio de trabajo del contenedor
COPY . .

# Define la instrucción para ejecutar la aplicación
# Numero de workers?
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]


# Crear imagen
#docker build -t apiclima .

# Ejecutar imagen
#docker run -d -p 8080:8080 apiclima

# VER = archivo de HistoricoBulk, directorio de Logs

#docker ps
#docker logs CONTAINER ID
#docker exec CONTAINER ID date
