from datetime import datetime
import time
import requests
from sqlalchemy import and_

from apiClima.app import scheduler
from apiClima.src.api.Data_day import climaRequest
from apiClima.src.api.history_hour_api import insert_history_hour_api, create_history_hour_table
import logging
from requests.exceptions import ConnectionError, HTTPError, RequestException
from urllib3.exceptions import ProtocolError

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')
#@scheduler.task('cron', id='job_cron_midnight', hour='00', minute='1')
@scheduler.task('cron', id='job_cron_hourly_except_midnight', minute='*/3')
def climaRequestDayliAndFuture():
    from apiClima.app import Distritos, Configuraciones, app, db, DiarioDia, FuturoDia, CantidadLlamadas
    with app.app_context():
        logger.info('Ejecutando carga de pronóstico diario y futuro')
        global parameters
        url = "https://api.openweathermap.org/data/3.0/onecall"
        contador = 0

        # Obtener todos los distritos activos
        distritos_activos = db.session.query(Distritos).filter_by(activo=True).all()
        print(distritos_activos)

        # Limpiar la tabla DiarioDia antes de insertar nuevos datos
        try:
            num_rows_deleted = db.session.query(DiarioDia).delete()
            db.session.commit()
            logger.info(f"Tabla DiarioDia truncada, {num_rows_deleted} filas eliminadas.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al truncar la tabla: {e}")
            return  # Detener la ejecución si no se puede truncar la tabla

        # Limpiar la tabla FuturoDia antes de insertar nuevos datos
        try:
            num_rows_deleted = db.session.query(FuturoDia).delete()
            db.session.commit()
            logger.info(f"Tabla FuturoDia truncada, {num_rows_deleted} filas eliminadas.")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al truncar la tabla: {e}")
            return  # Detener la ejecución si no se puede truncar la tabla


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
                response = requests.get(url, params=parameters)

                if response.status_code == 200:
                    contador += 1
                    logger.info("OpenWeather ha retornado código 200")
                    data = response.json()
                    print(data)
                    climaRequest(data, distrito.id)
                    logger.info('Tablas futuro_dia y diario_dia cargadas')
                    logger.info('Iniciando carga  las 00 para las horas')
                    insert_history_hour_api(distrito.id, data)
                    logger.info('Tablas de granuralidad horaria cargadas')


            except (ConnectionError, ProtocolError, HTTPError, RequestException) as e:
                logger.error(f'Error al hacer request a OpenWeather: {e}')
                # La API está caída, usar el último registro válido
                last_data = get_last_record_for_district(distrito.id)
                if last_data:
                    insert_history_hour_api(distrito.id, last_data)
                else:
                    logger.info(f"No hay datos históricos para el distrito {distrito.id}")


            # Cada 50 llamadas, pausa durante 60 segundos
            if contador % 50 == 0:
                logger.info(f'Pausa después de {contador} llamadas para evitar sobrepasar el límite de la API.')
                time.sleep(60)  # Pausa de 1 minuto###

        logger.info(f"FINALIZANDO TAREA DE CARGA DE DIARIO Y FUTURO. Cantidad de llamadas realizadas {contador}")
        nuevo_registro = CantidadLlamadas(
            cantidad_llamadas=contador,
            fecha=time.strftime('%Y-%m-%d')
        )

        # Añadir el nuevo registro a la sesión de la base de datos
        db.session.add(nuevo_registro)

        # Guardar los cambios en la base de datos
        db.session.commit()
        print(f"El registro de cantidad de llamadas de la fecha {nuevo_registro.fecha}, añadiendo una cantidad de {contador} llamadas en carga de diario y futuro")






def get_last_record_for_district(id_distrito):
    # Primero, obtén el modelo correcto para el distrito dado
    logger.info("Obteniendo el modelo para el distrito {}".format(id_distrito))
    HistoryModel = create_history_hour_table(id_distrito)
    logger.info(f"Modelo {HistoryModel} encontrado para el distrito".format(id_distrito))

    # Luego, consulta el último registro para ese modelo
    logger.info("Realizando la consulta del ultimo registro")
    last_record = HistoryModel.query.order_by(HistoryModel.update_datetime.desc()).first()

    if last_record:
        logger.info(f"Encontrado el ultimo registro{last_record}")
        # Si hay un registro, extrae los datos necesarios para replicar en un nuevo registro
        date_string = time.strftime('%Y-%m-%d %H:%M:%S')
        date_time_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        timestamp = date_time_obj.timestamp()
        data = {
            "current": {
                "dt": timestamp,  # Convierte datetime a timestamp
                "sunrise": last_record.sunrise,
                "sunset": last_record.sunset,
                "temp": last_record.temp,
                "feels_like": last_record.feels_like,
                "pressure": last_record.pressure,
                "humidity": last_record.humidity,
                "dew_point": last_record.dew_point,
                "uvi": last_record.uvi,
                "clouds": last_record.clouds,
                "visibility": last_record.visibility,
                "wind_speed": last_record.wind_speed,
                "wind_deg": last_record.wind_deg,
                "weather": [{
                    "description": last_record.weather_description
                }]
            }
        }
        return data
    logger.info("No existe el ultimo registro")
    return None


def verificar_registros_fecha(modelo, fecha_consulta, id_distrito):
    # Convertir la cadena de fecha a una estructura de tiempo
    fecha_inicio_struct = time.strptime(fecha_consulta, '%Y-%m-%d')

    # Convertir la estructura de tiempo a una fecha y hora completa (00:00:00)
    fecha_inicio = time.mktime(fecha_inicio_struct)

    # Crear la fecha de fin (23:59:59 del mismo día)
    fecha_fin_struct = time.strptime(fecha_consulta + " 23:59:59", '%Y-%m-%d %H:%M:%S')
    fecha_fin = time.mktime(fecha_fin_struct)

    # Convertir las marcas de tiempo a objetos datetime para la consulta
    fecha_inicio_dt = datetime.fromtimestamp(fecha_inicio)
    fecha_fin_dt = datetime.fromtimestamp(fecha_fin)

    # Realizar la consulta en la base de datos si ya existen registros cargados en la fecha con un distrito especifico

    registros = modelo.query.filter(
        and_(
            modelo.district_id == id_distrito,
            modelo.update_datetime.between(fecha_inicio_dt, fecha_fin_dt)
        )
    ).all()
    return len(registros) <= 0
