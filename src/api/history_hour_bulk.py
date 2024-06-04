import pandas as pd
import os
from app import db, scheduler, app  # Importa db, scheduler y app desde app.py

def load_csv_to_db(file_path):
    # Leer el archivo CSV
    data = pd.read_csv(file_path)

    # Obtener el nombre del archivo sin la extensión
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # Crear una clase dinámica para la tabla
    class DynamicTable(db.Model):
        __tablename__ = table_name
        id = db.Column(db.Integer, primary_key=True)
        # Crear dinámicamente columnas basadas en los encabezados del CSV
        for column in data.columns:
            vars()[column] = db.Column(db.String, nullable=True)

    # Crear la tabla en la base de datos con extend_existing=True
    table = DynamicTable.__table__
    table.metadata.create_all(db.engine, checkfirst=True)

    # Insertar los datos del CSV en la tabla
    data.to_sql(table_name, con=db.engine, if_exists='append', index=False)
    print(f'Tabla {table_name} creada y datos insertados exitosamente.')

@scheduler.task('cron', id='job_cron', minute='*/1')
def tarea_programada():
    with app.app_context():  # Asegura que la tarea se ejecute dentro del contexto de la aplicación Flask
        file_path = 'C:\\Users\\Konecta NB000114\\Documents\\ITAKYRY.csv'  # Actualiza esta ruta al archivo CSV
        load_csv_to_db(file_path)
        print('Tarea programada ejecutada.')
