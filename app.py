import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

from src.util.archivo import rebuild_dynamic_models
from src.util.log import setup_logger

setup_logger()

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')

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


# Función para iniciar el scheduler
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler iniciado.")
    else:
        logger.info("Scheduler ya está en ejecución.")


# Importa las tareas después de configurar el scheduler
import src.api.history_hour_bulk
import src.shedules.shedule_historico_bulk
import src.shedules.shedule_only_hour
import src.shedules.shedule_day_future_hour


# Definición de modelos para las tablas en base de datos
class Configuraciones(db.Model):
    __tablename__ = 'configuraciones'
    id = db.Column(db.Integer, primary_key=True)
    parametro = db.Column(db.String)
    valor = db.Column(db.String)
    fecha_hora_actualizacion = db.Column(db.DateTime)


class CantidadLlamadas(db.Model):
    __tablename__ = 'cantidad_llamadas'
    id = db.Column(db.Integer, primary_key=True)
    cantidad_llamadas = db.Column(db.Integer)
    fecha = db.Column(db.DateTime)


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
    moon_phase = db.Column(db.String)
    temp_max = db.Column(db.String)
    temp_min = db.Column(db.String)
    temp_morn = db.Column(db.String)
    temp_day = db.Column(db.String)
    temp_eve = db.Column(db.String)
    temp_night = db.Column(db.String)
    feels_like_morn = db.Column(db.String)
    feels_like_day = db.Column(db.String)
    feels_like_eve = db.Column(db.String)
    feels_like_night = db.Column(db.String)
    pressure = db.Column(db.String)
    humidity = db.Column(db.String)
    dew_point = db.Column(db.String)
    wind_speed = db.Column(db.String)
    wind_gust = db.Column(db.String)
    wind_deg = db.Column(db.String)
    weather_description = db.Column(db.String)
    clouds = db.Column(db.String)
    pop = db.Column(db.String)
    rain = db.Column(db.String)
    snow = db.Column(db.String)
    uvi = db.Column(db.String)


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
    moon_phase = db.Column(db.String)
    temp_max = db.Column(db.String)
    temp_min = db.Column(db.String)
    temp_morn = db.Column(db.String)
    temp_day = db.Column(db.String)
    temp_eve = db.Column(db.String)
    temp_night = db.Column(db.String)
    feels_like_morn = db.Column(db.String)
    feels_like_day = db.Column(db.String)
    feels_like_eve = db.Column(db.String)
    feels_like_night = db.Column(db.String)
    pressure = db.Column(db.String)
    humidity = db.Column(db.String)
    dew_point = db.Column(db.String)
    wind_speed = db.Column(db.String)
    wind_gust = db.Column(db.String)
    wind_deg = db.Column(db.String)
    weather_description = db.Column(db.String)
    clouds = db.Column(db.String)
    pop = db.Column(db.String)
    rain = db.Column(db.String)
    snow = db.Column(db.String)
    uvi = db.Column(db.String)


class FuturoDiaContingencia(db.Model):
    __tablename__ = 'futuro_dia_contingencia'
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.Integer, db.ForeignKey('distritos.id'))
    update_datetime = db.Column(db.DateTime)
    date = db.Column(db.String)
    sunrise = db.Column(db.String)
    sunset = db.Column(db.String)
    moonrise = db.Column(db.String)
    moonset = db.Column(db.String)
    moon_phase = db.Column(db.String)
    temp_max = db.Column(db.String)
    temp_min = db.Column(db.String)
    temp_morn = db.Column(db.String)
    temp_day = db.Column(db.String)
    temp_eve = db.Column(db.String)
    temp_night = db.Column(db.String)
    feels_like_morn = db.Column(db.String)
    feels_like_day = db.Column(db.String)
    feels_like_eve = db.Column(db.String)
    feels_like_night = db.Column(db.String)
    pressure = db.Column(db.String)
    humidity = db.Column(db.String)
    dew_point = db.Column(db.String)
    wind_speed = db.Column(db.String)
    wind_gust = db.Column(db.String)
    wind_deg = db.Column(db.String)
    weather_description = db.Column(db.String)
    clouds = db.Column(db.String)
    pop = db.Column(db.String)
    rain = db.Column(db.String)
    snow = db.Column(db.String)
    uvi = db.Column(db.String)


from sqlalchemy import inspect


@app.route('/')
def index():
    return "¡Bienvenido a la API del Clima!"

def initialize_application():
    with app.app_context():
        db.create_all()  # Opcional: remover en producción si se manejan migraciones.
    rebuild_dynamic_models()
    logger.info("Configuraciones inicializadas.")
    start_scheduler()


initialize_application()




# import logging
# from flask import Flask, jsonify
# from flask_apscheduler import APScheduler
# from datetime import datetime
# import pytz
#
# # Configura el logger
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('ApiClima')
#
# app = Flask(__name__)
#
# # Configuración del scheduler
# class Config:
#     SCHEDULER_API_ENABLED = True
#     SCHEDULER_TIMEZONE = 'America/Asuncion'
#
# app.config.from_object(Config())
# scheduler = APScheduler()
# scheduler.init_app(app)
#
# # Obtener la zona horaria local
# local_timezone = pytz.timezone(app.config['SCHEDULER_TIMEZONE'])
#
# @scheduler.task('interval', id='job_interval_example', seconds=30, misfire_grace_time=3000)
# def example_job():
#     logger.info(f'Tarea programada "example_job" ejecutada a las {datetime.now(local_timezone)}')
#
# if not scheduler.running:
#     scheduler.start()
#     logger.info("Scheduler iniciado.")
# else:
#     logger.info("Scheduler ya está en ejecución.")
#
# @app.route('/')
# def index():
#     return "¡Bienvenido a la API del Clima!"
#
# @app.route('/scheduler/jobs')
# def list_jobs():
#     jobs = scheduler.get_jobs()
#     jobs_info = []
#     for job in jobs:
#         jobs_info.append({
#             'id': job.id,
#             'next_run_time': str(job.next_run_time)
#         })
#     return jsonify(jobs_info)