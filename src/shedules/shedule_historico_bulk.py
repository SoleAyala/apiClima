import os
from apiClima.src.api.history_hour_bulk import load_csv_to_db, logger
import glob
from apiClima.app import scheduler, db


@scheduler.task('cron', id='job_cron', hour='02', minute='30')
def carga_historico_hora_bulk():
    from apiClima.app import app, Configuraciones
    logger.info("Iniciando carga de archivos csv desde el directorio")
    with app.app_context():
        configuracion = db.session.query(Configuraciones).filter_by(parametro='path_bulk_procesar').first()
        print("Iniciando")
        if configuracion:
            directory_path = configuracion.valor + '\\*.csv'
            logger.info(f"Ruta de directorio obtenida de configuración: {directory_path}")
        else:
            logger.error("No se encontró la configuración para 'path_bulk_procesar'")
            directory_path = None

        # Verificar si la ruta tiene barras invertidas y normalizarlas
        if os.name == 'nt':  # Si está en Windows
            directory_path = directory_path.replace('/', '\\')
            logger.info(f"Actualizada la ruta para Windows: {directory_path}")
        else:  # Para sistemas Unix (Linux, macOS)
            directory_path = directory_path.replace('\\', '/')
            logger.info(f"Actualizada la ruta para Linux: {directory_path}")


        if directory_path:
            csv_files = glob.glob(directory_path)
            logger.info(f"Archivos CSV encontrados: {csv_files}")
        else:
            csv_files = []

        if len(csv_files) == 0:
            logger.info("No existen archivos csv a procesar ")

        for file_path in csv_files:
            try:
                logger.info(f"Procesando archivo: {file_path}")
                load_csv_to_db(file_path)
            except Exception as e:
                logger.error(f"Error al procesar el archivo {file_path}: {e}")

        logger.info("Finalizado el proceso de carga de archivos csv")
