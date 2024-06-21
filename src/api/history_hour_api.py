import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from apiClima.app import db

dynamic_models = {}

def create_history_hour_table(id):
    class_name = f"HistoricoHoraApiClimaID{id}"
    table_name = f"historico_hora_api_clima_{id}"

    # Verifica si la tabla ya existe en el registro
    if table_name in dynamic_models:
        if dynamic_models[table_name] is None:  # La tabla existe, pero el modelo no está cargado
            # Carga el modelo si aún no está creado
            model = create_model_for_table(table_name, class_name)
            dynamic_models[table_name] = model
            return model
        return dynamic_models[table_name]

    # Si la tabla no está en el registro y no estamos seguros de que exista, verifica y posiblemente crear
    if not db.inspect(db.engine).has_table(table_name):
        # Crear el modelo y la tabla si no existen
        model = create_model_for_table(table_name, class_name)
        db.create_all()
        dynamic_models[table_name] = model
        return model
    else:
        # La tabla existe pero no estaba en dynamic_models, cargar el modelo
        model = create_model_for_table(table_name, class_name)
        dynamic_models[table_name] = model
        return model


def create_model_for_table(table_name, class_name):
    """Crea una definición de modelo dinámico basada en el nombre de la tabla y la clase."""
    attrs = {
        '__tablename__': table_name,
        'id': Column(Integer, primary_key=True),
        'update_datetime': Column(DateTime),
        'sunrise': Column(Integer),
        'sunset': Column(Integer),
        'temp': Column(Float),
        'feels_like': Column(Float),
        'pressure': Column(Integer),
        'humidity': Column(Integer),
        'dew_point': Column(Float),
        'uvi': Column(Integer),
        'clouds': Column(Integer),
        'visibility': Column(Integer),
        'wind_speed': Column(Float),
        'wind_deg': Column(Integer),
        'rain_1h': Column(Float),
        'wind_gust': Column(Float),
        'weather_description': Column(String)
    }
    return type(class_name, (db.Model,), attrs)

def insert_history_hour_api(id_distrito, data):
    current = data["current"]
    Table = create_history_hour_table(id_distrito)
    if Table:
        weather_instance = Table(
            update_datetime=datetime.datetime.fromtimestamp(current["dt"]),
            sunrise=current["sunrise"],
            sunset=current["sunset"],
            temp=current["temp"],
            feels_like=current["feels_like"],
            pressure=current["pressure"],
            humidity=current["humidity"],
            dew_point=current["dew_point"],
            uvi=int(current["uvi"]),
            clouds=current["clouds"],
            visibility=current["visibility"],
            wind_speed=current["wind_speed"],
            wind_deg=current["wind_deg"],
            rain_1h=current.get("rain", {}).get("1h", 0),
            wind_gust=current.get("wind_gust", 0),
            weather_description=current["weather"][0]["description"]
        )
        db.session.add(weather_instance)
        db.session.commit()
