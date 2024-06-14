import datetime
import time

import requests
from apiClima.app import scheduler, Distritos, DiarioDia, FuturoDia
from apiClima.src.api.Data_day import  cargaTablaDiarioDia, cargaTablaFuturoDia
from apiClima.src.api.history_hour_api import insert_history_hour_api
import logging

from apiClima.src.shedules.shedule_day_future_hour import verificar_registros_fecha, get_last_record_for_district

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')


@scheduler.task('cron', id='job_cron_hourly_except_midnight', hour='1-23', minute=1)
def climaRequestDayliAndFuture():
    global parameters
    url = "https://api.openweathermap.org/data/3.0/onecall"
    contador = 0

    # Obtener todos los distritos activos
    distritos_activos = Distritos.query.filter_by(activo=True).all()

    for distrito in distritos_activos:
        parameters = {
            'lat': distrito.latitud,
            'lon': distrito.longitud,
            'appid': distrito.appid,
            'units': 'metric',  # Celsius
            'lang': 'es',  # Español
        }

        response = requests.get(url, params=parameters)

        if response.status_code == 200:
            logger.info("OpenWeather ha retornado código 200")
            data = response.json()
            insert_history_hour_api(distrito.id, data)

            if verificar_registros_fecha(DiarioDia, datetime.date.today().isoformat()):
                logger.info(f'Se realizará la carga de la tabla diario_dia  desde la consulta de horas, Hora:{datetime.datetime}')
                daily_data = data['daily']
                # Datos del primer día (día actual)
                day = daily_data[0]
                cargaTablaDiarioDia(day)

            if verificar_registros_fecha(FuturoDia, datetime.date.today.isoformat()):
                logger.info(f'Se realizará la carga de la tabla futuro_dia desde la consulta de horas, Hora:{datetime.datetime}')
                cargaTablaFuturoDia(data)
        else:

            # La API está caída, usar el último registro válido
            last_data = get_last_record_for_district(distrito.id)
            if last_data:
                insert_history_hour_api(distrito.id, last_data)
            else:
                logger.info(f"No hay datos históricos para el distrito {distrito.id}")
            logger.error(f'OpenWeather presenta problemas en el request: {response.status_code}')
        contador += 1
        # Cada 50 llamadas, pausa durante 60 segundos
        if contador % 50 == 0:
            logger.info(f'Pausa después de {contador} llamadas para evitar sobrepasar el límite de la API.')
            time.sleep(60)  # Pausa de 1 minuto
