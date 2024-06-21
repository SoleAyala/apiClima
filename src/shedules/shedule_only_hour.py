
import time
import requests
from apiClima.app import scheduler, app, db
from apiClima.src.api.Data_day import  climaRequest
from apiClima.src.api.history_hour_api import insert_history_hour_api
import logging
from apiClima.src.shedules.shedule_day_future_hour import verificar_registros_fecha, get_last_record_for_district

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')


#@scheduler.task('cron', id='job_cron_hourly_except_midnight', hour='1-23', minute=1)
@scheduler.task('cron', id='job_cron_hourly_except_midnight', minute='*/4')
def climaRequestDayliAndFuture():
    from apiClima.app import Distritos, DiarioDia, FuturoDia, Configuraciones
    with app.app_context():
        global parameters
        fecha_hoy = time.strftime('%Y-%m-%d')
        url = "https://api.openweathermap.org/data/3.0/onecall"
        contador = 0
        appid = ''
        # Obtener todos los distritos activos
        distritos_activos = db.session.query(Distritos).filter_by(activo=True).all()

        for distrito in distritos_activos:
            appid = db.session.query(Configuraciones).filter_by(parametro=distrito.appid).first().valor
            parameters = {
                'lat': distrito.latitud,
                'lon': distrito.longitud,
                'appid': appid,
                'units': 'metric',  # Celsius
                'lang': 'es',  # Español
            }

            response = requests.get(url, params=parameters)

            if response.status_code == 200:
                logger.info("OpenWeather ha retornado código 200")
                data = response.json()
                logger.info(f"Creando para el id {distrito.id}")
                insert_history_hour_api(distrito.id, data)

                if verificar_registros_fecha(DiarioDia, fecha_hoy) and verificar_registros_fecha(FuturoDia, fecha_hoy):
                    logger.info(f"Se realizará la carga de la tabla diario_dia y futuro_dia desde la consulta de horas, Hora:{time.strftime('%Y-%m-%d %H:%M:%S)}')}")
                    climaRequest(data)

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

    logger.info("FINALIZANDO TAREA DE CARGA DE HORAS")
