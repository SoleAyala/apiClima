import time
import logging

from src.util.time import timestampToDate

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')


def climaRequest(data, distrito_id):
    # Obtención de los datos de la sección 'daily'
    daily_data = data['daily']
    # Datos del primer día (día actual)
    day = daily_data[0]
    cargaTablaDiarioDia(day, distrito_id)
    cargaTablaFuturoDia(daily_data, distrito_id)


def cargaTablaDiarioDia(day, distrito_id):
    from app import DiarioDia, db, Distritos

    fecha = day.get('dt')
    salida_sol = day.get('sunrise')
    puesta_sol = day.get('sunset')
    salida_luna = day.get('moonrise')
    puesta_luna = day.get('moonset')
    fase_lunar = day.get('moon_phase')
    temp_maxima = day.get('temp', {}).get('max')
    temp_minima = day.get('temp', {}).get('min')
    temp_manana = day.get('temp', {}).get('morn')
    temp_diurna = day.get('temp', {}).get('day')
    temp_tarde = day.get('temp', {}).get('eve')
    temp_nocturna = day.get('temp', {}).get('night')
    sensacion_manana = day.get('feels_like', {}).get('morn')
    sensacion_diurna = day.get('feels_like', {}).get('day')
    sensacion_tarde = day.get('feels_like', {}).get('eve')
    sensacion_nocturna = day.get('feels_like', {}).get('night')
    presion_atmosferica = day.get('pressure')
    humedad = day.get('humidity')
    punto_rocio = day.get('dew_point')
    velocidad_viento = day.get('wind_speed')
    rafagas_viento = day.get('wind_gust')
    direccion_viento = day.get('wind_deg')
    descripcion_clima = day.get('weather', [{}])[0].get('description')
    nubosidad = day.get('clouds')
    prob_precipitacion = day.get('pop')
    volumen_lluvia = day.get('rain')
    volumen_nieve = day.get('snow')
    indice_uv = day.get('uvi')
    fecha_hora_actualizacion = time.strftime('%Y-%m-%d %H:%M:%S')

    # Crear una instancia del modelo DiarioDia
    nuevo_registro = DiarioDia(
        district_id=distrito_id,
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

    # Verificar si fecha_carga_bulk está vacía
    distrito = Distritos.query.get(distrito_id)
    if distrito.fecha_ini_apiclima is None:
        distrito.fecha_ini_apiclima = time.strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()

    # Guardar en la base de datos
    db.session.add(nuevo_registro)
    db.session.commit()
    logger.info("Carga Tabla diario_dia realizada")


def cargaTablaFuturoDia(data, distrito_id):
    from apiClima.app import db, FuturoDia, Distritos

    # Verificar si fecha_ini_apiclima está vacía
    distrito = Distritos.query.get(distrito_id)
    if distrito.fecha_ini_apiclima is None:
        distrito.fecha_ini_apiclima = time.strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()


    contador = 0
    for day in data[1:]:
        contador = contador + 1
        # print(f"Cargando dato {contador}")
        fecha = day.get('dt')
        salida_sol = day.get('sunrise')
        puesta_sol = day.get('sunset')
        salida_luna = day.get('moonrise')
        puesta_luna = day.get('moonset')
        fase_lunar = day.get('moon_phase')
        temp_maxima = day.get('temp', {}).get('max')
        temp_minima = day.get('temp', {}).get('min')
        temp_manana = day.get('temp', {}).get('morn')
        temp_diurna = day.get('temp', {}).get('day')
        temp_tarde = day.get('temp', {}).get('eve')
        temp_nocturna = day.get('temp', {}).get('night')
        sensacion_manana = day.get('feels_like', {}).get('morn')
        sensacion_diurna = day.get('feels_like', {}).get('day')
        sensacion_tarde = day.get('feels_like', {}).get('eve')
        sensacion_nocturna = day.get('feels_like', {}).get('night')
        presion_atmosferica = day.get('pressure')
        humedad = day.get('humidity')
        punto_rocio = day.get('dew_point')
        velocidad_viento = day.get('wind_speed')
        rafagas_viento = day.get('wind_gust')
        direccion_viento = day.get('wind_deg')
        descripcion_clima = day.get('weather', [{}])[0].get('description')
        nubosidad = day.get('clouds')
        prob_precipitacion = day.get('pop')
        volumen_lluvia = day.get('rain')
        volumen_nieve = day.get('snow')
        indice_uv = day.get('uvi')
        fecha_hora_actualizacion = time.strftime('%Y-%m-%d %H:%M:%S')
        # Crear una instancia del modelo DiarioDia
        nuevo_registro = FuturoDia(
            district_id=distrito_id,
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

        # logger.info(f"Carga Tabla futuro_dia en el contador {contador} realizada")
    logger.info(f"Carga Tabla futuro_dia realizada")
