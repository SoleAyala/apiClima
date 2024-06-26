import time
import requests
import logging
from apiClima.app import scheduler, app, db
from requests.exceptions import ConnectionError, HTTPError, RequestException
from urllib3.exceptions import ProtocolError
from apiClima.src.api.Data_day import climaRequest
from apiClima.src.api.history_hour_api import insert_history_hour_api
from apiClima.src.shedules.shedule_day_future_hour import verificar_registros_fecha, get_last_record_for_district

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')


@scheduler.task('cron', id='job_cron_hourly_except_midnight', minute='*/4')
def climaRequestOnlyHour():
    from apiClima.app import Distritos, DiarioDia, FuturoDia, Configuraciones
    session = requests.Session()  # Usar una sesión para reutilizar conexiones
    with app.app_context():
        fecha_hoy = time.strftime('%Y-%m-%d')
        url = "https://api.openweathermap.org/data/3.0/onecall"
        contador = 0

        # Obtener todos los distritos activos
        distritos_activos = db.session.query(Distritos).filter_by(activo=True).all()

        for distrito in distritos_activos:
            try:
                appid = db.session.query(Configuraciones).filter_by(parametro=distrito.appid).first().valor
                parameters = {
                    'lat': distrito.latitud,
                    'lon': distrito.longitud,
                    'appid': appid,
                    'units': 'metric',  # Celsius
                    'lang': 'es',  # Español
                }

                response = session.get(url, params=parameters)
                response.raise_for_status()  # Verificar si la respuesta es un error

                if response.status_code == 200:
                    logger.info("OpenWeather ha retornado código 200")
                    data = response.json()
                    logger.info(f"Cargando para el Distrito con id {distrito.id} con dato {data}")
                    insert_history_hour_api(distrito.id, data)
                    contador += 1

                    if verificar_registros_fecha(DiarioDia, fecha_hoy, distrito.id):
                        logger.info(
                            f"Se realizará la carga de la tabla diario_dia y futuro_dia desde la consulta de horas, Hora:{time.strftime('%Y-%m-%d %H:%M:%S')}")
                        # Limpiar la tabla DiarioDia antes de insertar nuevos datos
                        try:
                            num_rows_deleted = db.session.query(DiarioDia).delete()
                            db.session.commit()
                            logger.info(f"Tabla DiarioDia truncada, {num_rows_deleted} filas eliminadas.")
                        except Exception as e:
                            db.session.rollback()
                            logger.error(f"Error al truncar la tabla: {e}")
                            return  # Detener la ejecución si no se puede truncar la tabla
                        climaRequest(data, distrito.id)

            except (ConnectionError, ProtocolError, HTTPError, RequestException) as e:
                logger.error(f'Error al hacer request a OpenWeather: {e}')
                last_data = get_last_record_for_district(distrito.id)
                logger.info(f"lastData encontrado: {last_data}")
                if last_data:
                    insert_history_hour_api(distrito.id, last_data)
                    logger.info("Se duplico el registro anterior ")
                else:
                    logger.info(f"No hay datos históricos para el distrito {distrito.id}")

            # Cada 50 llamadas, pausa durante 60 segundos
            if contador % 50 == 0:
                logger.info(f'Pausa después de {contador} llamadas para evitar sobrepasar el límite de la API.')
                time.sleep(60)  # Pausa de 1 minuto

        logger.info(f"FINALIZADO TAREA DE CARGA DE HORAS, Cantidad de llamadas igual a: {contador} ")
