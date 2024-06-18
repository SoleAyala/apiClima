import logging
from flask import Flask, app, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_apscheduler import APScheduler
import urllib.parse

from sqlalchemy import true

from apiClima.src.util.log import setup_logger





load_dotenv()  # Carga las variables de entorno desde el archivo .env
app = Flask(__name__)
#logger = setup_logger()  # Inicia el logger

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
scheduler.start()

# Importa las tareas después de configurar el scheduler
import apiClima.src.api.history_hour_bulk
import apiClima.src.shedules.shedule_historico_bulk
import apiClima.src.shedules.shedule_only_hour
import apiClima.src.shedules.shedule_only_hour

# Definición de modelos para las tablas en base de datos

@app.route('/')
def index():
    return "¡Bienvenido a la API del Clima!"



class Configuraciones(db.Model):
    __tablename__ = 'configuraciones'
    id = db.Column(db.Integer, primary_key=True)
    parametro = db.Column(db.String)
    valor = db.Column(db.String)
    fecha_hora_actualizacion = db.Column(db.DateTime)

class Distritos(db.Model):
    __tablename__ = 'distritos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    activo = db.Column(db.Boolean)
    departamento = db.Column(db.String)
    observacion = db.Column(db.String)
    region = db.Column(db.String)
    fecha_carga_bulk = db.Column(db.DateTime)
    fecha_ini_apiclima = db.Column(db.DateTime)
    appid = db.Column(db.String)

class DiarioDia(db.Model):
    __tablename__ = 'diario_dia'
    id = db.Column(db.Integer, primary_key=True)
    id_distrito = db.Column(db.Integer, db.ForeignKey('distritos.id'))
    fecha_hora_actualizacion = db.Column(db.DateTime)
    fecha = db.Column(db.String)
    salida_sol = db.Column(db.String)
    puesta_sol = db.Column(db.String)
    salida_luna = db.Column(db.String)
    puesta_luna = db.Column(db.String)
    fase_lunar = db.Column(db.String)
    temp_maxima = db.Column(db.String)
    temp_minima = db.Column(db.String)
    temp_manana = db.Column(db.String)
    temp_diurna = db.Column(db.String)
    temp_tarde = db.Column(db.String)
    temp_nocturna = db.Column(db.String)
    sensacion_manana = db.Column(db.String)
    sensacion_diurna = db.Column(db.String)
    sensacion_tarde = db.Column(db.String)
    sensacion_nocturna = db.Column(db.String)
    presion_atmosferica = db.Column(db.String)
    humedad = db.Column(db.String)
    punto_rocio = db.Column(db.String)
    velocidad_viento = db.Column(db.String)
    rafagas_viento = db.Column(db.String)
    direccion_viento = db.Column(db.String)
    descripcion_clima = db.Column(db.String)
    nubosidad = db.Column(db.String)
    prob_precipitacion = db.Column(db.String)
    volumen_lluvia = db.Column(db.String)
    volumen_nieve = db.Column(db.String)
    indice_uv = db.Column(db.String)

class FuturoDia(db.Model):
    __tablename__ = 'futuro_dia'
    id = db.Column(db.Integer, primary_key=True)
    id_distrito = db.Column(db.Integer, db.ForeignKey('distritos.id'))
    fecha_hora_actualizacion = db.Column(db.DateTime)
    fecha = db.Column(db.String)
    salida_sol = db.Column(db.String)
    puesta_sol = db.Column(db.String)
    salida_luna = db.Column(db.String)
    puesta_luna = db.Column(db.String)
    fase_lunar = db.Column(db.String)
    temp_maxima = db.Column(db.String)
    temp_minima = db.Column(db.String)
    temp_manana = db.Column(db.String)
    temp_diurna = db.Column(db.String)
    temp_tarde = db.Column(db.String)
    temp_nocturna = db.Column(db.String)
    sensacion_manana = db.Column(db.String)
    sensacion_diurna = db.Column(db.String)
    sensacion_tarde = db.Column(db.String)
    sensacion_nocturna = db.Column(db.String)
    presion_atmosferica = db.Column(db.String)
    humedad = db.Column(db.String)
    punto_rocio = db.Column(db.String)
    velocidad_viento = db.Column(db.String)
    rafagas_viento = db.Column(db.String)
    direccion_viento = db.Column(db.String)
    descripcion_clima = db.Column(db.String)
    nubosidad = db.Column(db.String)
    prob_precipitacion = db.Column(db.String)
    volumen_lluvia = db.Column(db.String)
    volumen_nieve = db.Column(db.String)
    indice_uv = db.Column(db.String)


if __name__ == "__main__":
    app.run(debug=True)
