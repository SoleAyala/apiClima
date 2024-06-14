import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_history_hour_table(id):
    class_name = f"historico_hora_api_clima_{id}"
    if class_name not in db.Model._decl_class_registry:
        attrs = {
            '__tablename__': f'historico_hora_api_clima_{id}',
            'id': db.Column(db.Integer, primary_key=True),
            'id_distrito': db.Column(db.Integer),
            'fecha_hora_actualizacion': db.Column(db.DateTime),
            'sunrise': db.Column(db.Integer),
            'sunset': db.Column(db.Integer),
            'temp': db.Column(db.Float),
            'feels_like': db.Column(db.Float),
            'pressure': db.Column(db.Integer),
            'humidity': db.Column(db.Integer),
            'dew_point': db.Column(db.Float),
            'uvi': db.Column(db.Integer),
            'clouds': db.Column(db.Integer),
            'visibility': db.Column(db.Integer),
            'wind_speed': db.Column(db.Float),
            'wind_deg': db.Column(db.Integer),
            'weather_description': db.Column(db.String)
        }
        model = type(class_name, (db.Model,), attrs)
        db.create_all()
        return model
    return getattr(db.Model, class_name)

def insert_history_hour_api(id_distrito, data):
    Table = create_history_hour_table(id_distrito)
    weather = Table(
        id_distrito=id_distrito,
        fecha_hora_actualizacion=datetime.datetime.fromtimestamp(data["current"]["dt"]),
        sunrise=data["current"]["sunrise"],
        sunset=data["current"]["sunset"],
        temp=data["current"]["temp"],
        feels_like=data["current"]["feels_like"],
        pressure=data["current"]["pressure"],
        humidity=data["current"]["humidity"],
        dew_point=data["current"]["dew_point"],
        uvi=int(data["current"]["uvi"]),
        clouds=data["current"]["clouds"],
        visibility=data["current"]["visibility"],
        wind_speed=data["current"]["wind_speed"],
        wind_deg=data["current"]["wind_deg"],
        weather_description=data["current"]["weather"][0]["description"]
    )
    db.session.add(weather)
    db.session.commit()

