from datetime import datetime
import logging

from apiClima.src.util.time import timestampToDate
# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')

def timestampToDate(timestamp, timezone_offset):
    return datetime.utcfromtimestamp(timestamp + timezone_offset).strftime('%Y-%m-%d %H:%M:%S')

def climaRequest(data):
    # Obtención de los datos de la sección 'daily'
    daily_data = data['daily']
    # Datos del primer día (día actual)
    day = daily_data[0]
    cargaTablaDiarioDia(day)
    cargaTablaFuturoDia(daily_data)



def  cargaTablaDiarioDia(day):
    from apiClima.app import DiarioDia, db
    # Limpiar la tabla FuturoDia antes de insertar nuevos datos
    try:
        num_rows_deleted = db.session.query(DiarioDia).delete()
        db.session.commit()
        logger.info(f"Tabla DiarioDia truncada, {num_rows_deleted} filas eliminadas.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al truncar la tabla: {e}")
        return  # Detener la ejecución si no se puede truncar la tabla

    fecha = day['dt']
    salida_sol = day['sunrise']
    puesta_sol = day['sunset']
    salida_luna = day.get('moonrise', 0)
    puesta_luna = day.get('moonset', 0)
    fase_lunar = day.get('moon_phase', 'No disponible')
    temp_maxima = day['temp']['max']
    temp_minima = day['temp']['min']
    temp_manana = day['temp']['morn']
    temp_diurna = day['temp']['day']
    temp_tarde = day['temp']['eve']
    temp_nocturna = day['temp']['night']
    sensacion_manana = day['feels_like']['morn']
    sensacion_diurna = day['feels_like']['day']
    sensacion_tarde = day['feels_like']['eve']
    sensacion_nocturna = day['feels_like']['night']
    presion_atmosferica = day['pressure']
    humedad = day['humidity']
    punto_rocio = day['dew_point']
    velocidad_viento = day['wind_speed']
    rafagas_viento = day.get('wind_gust', 0)
    direccion_viento = day['wind_deg']
    descripcion_clima = day['weather'][0]['description']
    nubosidad = day['clouds']
    prob_precipitacion = day['pop']
    volumen_lluvia = day.get('rain', 0)
    volumen_nieve = day.get('snow', 0)
    indice_uv = day['uvi']
    fecha_hora_actualizacion = datetime.utcnow()

    # Crear una instancia del modelo DiarioDia
    nuevo_registro = DiarioDia(
        district_id=1,
        update_datetime=fecha_hora_actualizacion,
        date=fecha,
        sunrise=salida_sol,
        sunset=puesta_sol,
        moonrise=salida_luna,
        moonset=puesta_luna,
        moon_phase=fase_lunar,
        temp_max=temp_maxima,
        temp_min=temp_minima,
        temp_morn=temp_manana,
        temp_day=temp_diurna,
        temp_eve=temp_tarde,
        temp_night=temp_nocturna,
        feels_like_morn=sensacion_manana,
        feels_like_day=sensacion_diurna,
        feels_like_eve=sensacion_tarde,
        feels_like_night=sensacion_nocturna,
        pressure=presion_atmosferica,
        humidity=humedad,
        dew_point=punto_rocio,
        wind_speed=velocidad_viento,
        wind_gust=rafagas_viento,
        wind_deg=direccion_viento,
        weather_description=descripcion_clima,
        clouds=nubosidad,
        pop=prob_precipitacion,
        rain=volumen_lluvia,
        snow=volumen_nieve,
        uvi=indice_uv
    )

    # Guardar en la base de datos
    db.session.add(nuevo_registro)
    db.session.commit()
    logger.info("Carga Tabla diario_dia realizada")


def cargaTablaFuturoDia(data):
    from apiClima.app import db, FuturoDia
    # Limpiar la tabla FuturoDia antes de insertar nuevos datos
    try:
        num_rows_deleted = db.session.query(FuturoDia).delete()
        db.session.commit()
        logger.info(f"Tabla FuturoDia truncada, {num_rows_deleted} filas eliminadas.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al truncar la tabla: {e}")
        return  # Detener la ejecución si no se puede truncar la tabla
    contador = 0
    for day in data[1:]:
        contador= contador+1
        print(f"Cargando dato {contador}")
        fecha = day['dt']
        salida_sol = day['sunrise']
        puesta_sol = day['sunset']
        salida_luna = day.get('moonrise', 0)
        puesta_luna = day.get('moonset', 0)
        fase_lunar = day.get('moon_phase', 'No disponible')
        temp_maxima = day['temp']['max']
        temp_minima = day['temp']['min']
        temp_manana = day['temp']['morn']
        temp_diurna = day['temp']['day']
        temp_tarde = day['temp']['eve']
        temp_nocturna = day['temp']['night']
        sensacion_manana = day['feels_like']['morn']
        sensacion_diurna = day['feels_like']['day']
        sensacion_tarde = day['feels_like']['eve']
        sensacion_nocturna = day['feels_like']['night']
        presion_atmosferica = day['pressure']
        humedad = day['humidity']
        punto_rocio = day['dew_point']
        velocidad_viento = day['wind_speed']
        rafagas_viento = day.get('wind_gust', 0)
        direccion_viento = day['wind_deg']
        descripcion_clima = day['weather'][0]['description']
        nubosidad = day['clouds']
        prob_precipitacion = day['pop']
        volumen_lluvia = day.get('rain', 0)
        volumen_nieve = day.get('snow', 0)
        indice_uv = day['uvi']
        fecha_hora_actualizacion = datetime.utcnow()

        # Crear una instancia del modelo DiarioDia
        nuevo_registro = FuturoDia(
            district_id=1,
            update_datetime=fecha_hora_actualizacion,
            date=fecha,
            sunrise=salida_sol,
            sunset=puesta_sol,
            moonrise=salida_luna,
            moonset=puesta_luna,
            moon_phase=fase_lunar,
            temp_max=temp_maxima,
            temp_min=temp_minima,
            temp_morn=temp_manana,
            temp_day=temp_diurna,
            temp_eve=temp_tarde,
            temp_night=temp_nocturna,
            feels_like_morn=sensacion_manana,
            feels_like_day=sensacion_diurna,
            feels_like_eve=sensacion_tarde,
            feels_like_night=sensacion_nocturna,
            pressure=presion_atmosferica,
            humidity=humedad,
            dew_point=punto_rocio,
            wind_speed=velocidad_viento,
            wind_gust=rafagas_viento,
            wind_deg=direccion_viento,
            weather_description=descripcion_clima,
            clouds=nubosidad,
            pop=prob_precipitacion,
            rain=volumen_lluvia,
            snow=volumen_nieve,
            uvi=indice_uv
        )


        # Guardar en la base de datos
        db.session.add(nuevo_registro)
        db.session.commit()

        logger.info(f"Carga Tabla futuro_dia en el contador {contador} realizada")


