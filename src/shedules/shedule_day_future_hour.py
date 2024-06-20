from datetime import datetime
import time
import requests
from apiClima.app import scheduler
from apiClima.src.api.Data_day import climaRequest
from apiClima.src.api.history_hour_api import insert_history_hour_api, create_history_hour_table
import logging


# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')
@scheduler.task('cron', id='job_cron_midnight', minute='*/5')
def climaRequestDayliAndFuture():
    from apiClima.app import Distritos, Configuraciones, app, db
    with app.app_context():
        logger.info('Ejecutando carga de pronóstico diario y futuro')
        global parameters
        url = "https://api.openweathermap.org/data/3.0/onecall"
        contador = 0

        # Obtener todos los distritos activos
        distritos_activos = db.session.query(Distritos).filter_by(activo=True).all()
        print(distritos_activos)

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
                print(data)
                climaRequest(data)
                logger.info('Tablas futuro_dia y diario_dia cargadas')
                logger.info('Iniciando carga  las 00 para las horas')
                insert_history_hour_api(distrito.id, data)
                logger.info('Tablas de granuralidad horaria cargadas')

            else:
                logger.error(f'OpenWeather presenta problemas en el request: {response.status_code}')
                # La API está caída, usar el último registro válido
                last_data = get_last_record_for_district(distrito.id)
                if last_data:
                    insert_history_hour_api(distrito.id, last_data)
                else:
                    logger.info(f"No hay datos históricos para el distrito {distrito.id}")

            contador += 1
            # Cada 50 llamadas, pausa durante 60 segundos
            if contador % 50 == 0:
                logger.info(f'Pausa después de {contador} llamadas para evitar sobrepasar el límite de la API.')
                time.sleep(60)  # Pausa de 1 minuto
        logger.info("FINALIZANDO TAREA DE CARGA DE DIARIO Y FUTURO")






def get_last_record_for_district(id_distrito):
    # Primero, obtén el modelo correcto para el distrito dado
    HistoryModel = create_history_hour_table(id_distrito)

    # Luego, consulta el último registro para ese modelo
    last_record = HistoryModel.query.filter_by(id_distrito=id_distrito).order_by(
        HistoryModel.fecha_hora_actualizacion.desc()).first()

    if last_record:
        # Si hay un registro, extrae los datos necesarios para replicar en un nuevo registro
        data = {
            "current": {
                "dt": last_record.fecha_hora_actualizacion.timestamp(),  # Convierte datetime a timestamp
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
    return None


def verificar_registros_fecha(modelo, fecha_consulta):
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

    # Realizar la consulta en la base de datos
    registros = modelo.query.filter(modelo.update_datetime.between(fecha_inicio_dt, fecha_fin_dt)).all()
    return len(registros) <= 0