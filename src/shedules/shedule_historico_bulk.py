from apiClima.src.api.history_hour_bulk import load_csv_to_db, logger
import glob
from apiClima.app import scheduler, db


@scheduler.task('cron', id='job_cron', minute='*/3')
def carga_historico_hora_bulk():
    from apiClima.app import app, Configuraciones
    logger.info("Iniciando carga de archivos csv desde el directorio")
    with app.app_context():
        # Busca todos los archivos CSV en el directorio especificado
        configuracion = db.session.query(Configuraciones).filter_by(parametro='path_bulk_procesar').first()
        print("Iniciando")
        if configuracion:
            # Accede al atributo 'valor' que debería contener la ruta.
            directory_path = configuracion.valor + '\\*.csv'
        else:
            # Maneja el caso donde no se encuentre la configuración.
            print("No se encontró la configuración para 'path_bulk_procesar'")
            directory_path = None  # O manejar de otra manera adecuada
        csv_files = glob.glob(directory_path)
        if(csv_files.__len__() > 0):
            logger.info("No ")
        # Procesa cada archivo encontrado
        for file_path in csv_files:
            load_csv_to_db(file_path)
        print("Finalizado el proceso de carga de archivos csv")