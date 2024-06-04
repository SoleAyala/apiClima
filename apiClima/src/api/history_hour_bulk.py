from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/databasename'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración del scheduler
app.config['SCHEDULER_API_ENABLED'] = True
db = SQLAlchemy(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


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

    # Crear la tabla en la base de datos
    db.create_all()

    # Insertar los datos del CSV en la tabla
    data.to_sql(table_name, con=db.engine, if_exists='append', index=False)
    print(f'Tabla {table_name} creada y datos insertados exitosamente.')


@scheduler.task('cron', id='job_cron', minute='*/1')
def tarea_programada():
    file_path = 'C:\\Users\\Konecta NB000114\\Documents\\YTAKYRY.csv'  # Actualiza esta ruta al archivo CSV
    load_csv_to_db(file_path)
    print('Tarea programada ejecutada.')


if __name__ == '__main__':
    # Verificar si el scheduler está configurado correctamente
    print('Scheduler configurado y la aplicación está corriendo.')
    app.run(debug=True)
