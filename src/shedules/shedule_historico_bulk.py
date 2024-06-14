from apiClima.app import scheduler, app
from apiClima.src.api.history_hour_bulk import load_csv_to_db
import glob


@scheduler.task('cron', id='job_cron_3am', hour='2', minute='30')
def carga_historico_hora_bulk():
    with app.app_context():
        # Busca todos los archivos CSV en el directorio especificado
        directory_path = 'C:\\Users\\Konecta NB000114\\Documents\\*.csv'
        csv_files = glob.glob(directory_path)

        # Procesa cada archivo encontrado
        for file_path in csv_files:
            load_csv_to_db(file_path)
