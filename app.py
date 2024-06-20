import logging
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

from apiClima.src.util.archivo import rebuild_dynamic_models
from apiClima.src.util.log import setup_logger

# Carga las variables de entorno desde el archivo .env
load_dotenv()
app = Flask(__name__)
dynamic_models = {}

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
import apiClima.src.shedules.shedule_day_future_hour


# Definición de modelos para las tablas en base de datos
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
    district_id = db.Column(db.Integer, db.ForeignKey('distritos.id'))
    update_datetime = db.Column(db.DateTime)
    date = db.Column(db.String)
    sunrise = db.Column(db.String)
    sunset = db.Column(db.String)
    moonrise = db.Column(db.String)
    moonset = db.Column(db.String)
    lunar_phase = db.Column(db.String)
    max_temp = db.Column(db.String)
    min_temp = db.Column(db.String)
    morning_temp = db.Column(db.String)
    day_temp = db.Column(db.String)
    afternoon_temp = db.Column(db.String)
    night_temp = db.Column(db.String)
    morning_feel = db.Column(db.String)
    day_feel = db.Column(db.String)
    afternoon_feel = db.Column(db.String)
    night_feel = db.Column(db.String)
    atmospheric_pressure = db.Column(db.String)
    humidity = db.Column(db.String)
    dew_point = db.Column(db.String)
    wind_speed = db.Column(db.String)
    wind_gusts = db.Column(db.String)
    wind_direction = db.Column(db.String)
    weather_description = db.Column(db.String)
    cloudiness = db.Column(db.String)
    precipitation_prob = db.Column(db.String)
    rain_volume = db.Column(db.String)
    snow_volume = db.Column(db.String)
    uv_index = db.Column(db.String)


class FuturoDia(db.Model):
    __tablename__ = 'futuro_dia'
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('distritos.id'))
    update_datetime = db.Column(db.DateTime)
    date = db.Column(db.String)
    sunrise = db.Column(db.String)
    sunset = db.Column(db.String)
    moonrise = db.Column(db.String)
    moonset = db.Column(db.String)
    lunar_phase = db.Column(db.String)
    max_temp = db.Column(db.String)
    min_temp = db.Column(db.String)
    morning_temp = db.Column(db.String)
    day_temp = db.Column(db.String)
    afternoon_temp = db.Column(db.String)
    night_temp = db.Column(db.String)
    morning_feel = db.Column(db.String)
    day_feel = db.Column(db.String)
    afternoon_feel = db.Column(db.String)
    night_feel = db.Column(db.String)
    atmospheric_pressure = db.Column(db.String)
    humidity = db.Column(db.String)
    dew_point = db.Column(db.String)
    wind_speed = db.Column(db.String)
    wind_gusts = db.Column(db.String)
    wind_direction = db.Column(db.String)
    weather_description = db.Column(db.String)
    cloudiness = db.Column(db.String)
    precipitation_prob = db.Column(db.String)
    rain_volume = db.Column(db.String)
    snow_volume = db.Column(db.String)
    uv_index = db.Column(db.String)


from sqlalchemy import inspect







@app.route('/')
def index():
    return "¡Bienvenido a la API del Clima!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    rebuild_dynamic_models()
    app.run(debug=True)

