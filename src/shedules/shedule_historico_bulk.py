from apiClima.app import scheduler, app, Configuraciones
from apiClima.src.api.history_hour_bulk import load_csv_to_db
import glob


@scheduler.task('cron', id='job_cron_3am', hour='2', minute='30')
def carga_historico_hora_bulk():
    with app.app_context():
        # Busca todos los archivos CSV en el directorio especificado
        path = Configuraciones.filter_by(parametro='path_bulk_procesar').first()
        directory_path = (path+'\\*.csv')
        csv_files = glob.glob(directory_path)

        # Procesa cada archivo encontrado
        for file_path in csv_files:
            load_csv_to_db(file_path)
