import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

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

# Modelo Clima existente
class Clima(db.Model):
    __tablename__ = 'clima'
    id = db.Column(db.Integer, primary_key=True)
    tem_min = db.Column(db.Float, nullable=False)
    tem_max = db.Column(db.Float, nullable=False)

# Nuevo Modelo Precipitacion
class Precipitacion(db.Model):
    __tablename__ = 'precipitacion'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(10), nullable=False)

# Nuevo Modelo Viento
class Viento(db.Model):
    __tablename__ = 'viento'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    velocidad = db.Column(db.Float, nullable=False)
    direccion = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return "¡Bienvenido a la API del Clima!"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
