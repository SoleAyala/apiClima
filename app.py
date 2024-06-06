# app.py
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

load_dotenv()  # Carga las variables de entorno desde el archivo .env

app = Flask(__name__)

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in the environment")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configuración del scheduler
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()  # Asegúrate de que el scheduler se inicie

# Logging
def setup_logger(app):
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

setup_logger(app)

# Importa las tareas después de configurar el scheduler
import src.api.history_hour_bulk

#DEFINICION DE MODELOS PARA LAS TABLAS EN BASE DE DATOS
class Diario_dia(db.Model):
    __tablename__ = 'Diario_día'
    Id = db.Column(db.Integer, primary_key=True)
    ID_Distrito = db.Column(db.Integer, nullable=False)
    Fecha_Hora_Actualización = db.Column(db.DateTime, nullable=False)
    Fecha = db.Column(db.String, nullable=False)
    Salida_Sol = db.Column(db.String, nullable=False)
    Puesta_Sol = db.Column(db.String, nullable=False)
    Salida_Luna = db.Column(db.String, nullable=False)
    Puesta_Luna = db.Column(db.String, nullable=False)
    Fase_Lunar = db.Column(db.String, nullable=False)
    Temp_Maxima = db.Column(db.String, nullable=False)
    Temp_Minima = db.Column(db.String, nullable=False)
    Temp_Mañana = db.Column(db.String, nullable=False)
    Temp_Diurna = db.Column(db.String, nullable=False)
    Temp_Tarde = db.Column(db.String, nullable=False)
    Temp_Nocturna = db.Column(db.String, nullable=False)
    Sensacion_Mañana = db.Column(db.String, nullable=False)
    Sensacion_Diurna = db.Column(db.String, nullable=False)
    Sensacion_Tarde = db.Column(db.String, nullable=False)
    Sensacion_Nocturna = db.Column(db.String, nullable=False)
    Presion_Atmosferica = db.Column(db.String, nullable=False)
    Humedad = db.Column(db.String, nullable=False)
    Punto_Rocio = db.Column(db.String, nullable=False)
    Velocidad_Viento = db.Column(db.String, nullable=False)
    Rafagas_Viento = db.Column(db.String, nullable=False)
    Direccion_Viento = db.Column(db.String, nullable=False)
    Descripcion_Clima = db.Column(db.String, nullable=False)
    Nubosidad = db.Column(db.String, nullable=False)
    Prob_Precipitacion = db.Column(db.String, nullable=False)
    Volumen_Lluvia = db.Column(db.String, nullable=False)
    Volumen_Nieve = db.Column(db.String, nullable=False)
    Indice_UV = db.Column(db.String, nullable=False)


class Futuro_dia(db.Model):
    __tablename__ = 'Diario_día'
    Id = db.Column(db.Integer, primary_key=True)
    ID_Distrito = db.Column(db.Integer, nullable=False)
    Fecha_Hora_Actualización = db.Column(db.DateTime, nullable=False)
    Fecha = db.Column(db.String, nullable=False)
    Salida_Sol = db.Column(db.String, nullable=False)
    Puesta_Sol = db.Column(db.String, nullable=False)
    Salida_Luna = db.Column(db.String, nullable=False)
    Puesta_Luna = db.Column(db.String, nullable=False)
    Fase_Lunar = db.Column(db.String, nullable=False)
    Temp_Maxima = db.Column(db.String, nullable=False)
    Temp_Minima = db.Column(db.String, nullable=False)
    Temp_Mañana = db.Column(db.String, nullable=False)
    Temp_Diurna = db.Column(db.String, nullable=False)
    Temp_Tarde = db.Column(db.String, nullable=False)
    Temp_Nocturna = db.Column(db.String, nullable=False)
    Sensacion_Mañana = db.Column(db.String, nullable=False)
    Sensacion_Diurna = db.Column(db.String, nullable=False)
    Sensacion_Tarde = db.Column(db.String, nullable=False)
    Sensacion_Nocturna = db.Column(db.String, nullable=False)
    Presion_Atmosferica = db.Column(db.String, nullable=False)
    Humedad = db.Column(db.String, nullable=False)
    Punto_Rocio = db.Column(db.String, nullable=False)
    Velocidad_Viento = db.Column(db.String, nullable=False)
    Rafagas_Viento = db.Column(db.String, nullable=False)
    Direccion_Viento = db.Column(db.String, nullable=False)
    Descripcion_Clima = db.Column(db.String, nullable=False)
    Nubosidad = db.Column(db.String, nullable=False)
    Prob_Precipitacion = db.Column(db.String, nullable=False)
    Volumen_Lluvia = db.Column(db.String, nullable=False)
    Volumen_Nieve = db.Column(db.String, nullable=False)
    Indice_UV = db.Column(db.String, nullable=False)


class Histórico_hora_api_clima(db.Model):
    __tablename__ = 'Histórico_hora_api_clima'
    Id = db.Column(db.Integer, primary_key=True)
    ID_Distrito = db.Column(db.Integer, nullable=False)
    Fecha_Hora_Actualización = db.Column(db.DateTime, nullable=False)
    Sunrise = db.Column(db.Integer, nullable=False)
    Sunset = db.Column(db.Integer, nullable=False)
    Temp = db.Column(db.Float, nullable=False)
    Feels_Like = db.Column(db.Float, nullable=False)
    Pressure = db.Column(db.Integer, nullable=False)
    Humidity = db.Column(db.Integer, nullable=False)
    Dew_Point = db.Column(db.Float, nullable=False)
    Uvi = db.Column(db.Integer, nullable=False)
    Clouds = db.Column(db.Integer, nullable=False)
    Visibility = db.Column(db.Integer, nullable=False)
    Wind_Speed = db.Column(db.Float, nullable=False)
    Wind_Deg = db.Column(db.Integer, nullable=False)
    Weather_Description = db.Column(db.String, nullable=False)


class Configuraciones(db.Model):
    __tablename__ = 'Configuraciones'
    Id = db.Column(db.Integer, primary_key=True)
    Parámetro = db.Column(db.String, nullable=False)
    Valor = db.Column(db.String, nullable=False)
    Fecha_Hora_Actualización = db.Column(db.DateTime, nullable=False)

class Distritos(db.Model):
    __tablename__ = 'Distritos'
    Id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String, nullable=False)
    Latitud = db.Column(db.Float, nullable=False)
    Longitud = db.Column(db.Float, nullable=False)
    Activo = db.Column(db.Boolean, nullable=False)
    Departamento = db.Column(db.String)
    Observación = db.Column(db.String)
    Región = db.Column(db.String)
    Fecha_Carga_Bulk = db.Column(db.DateTime)
    Fecha_Ini_ApiClima = db.Column(db.DateTime)
    Appid = db.Column(db.String)




if __name__ == "__main__":
    app.run()
