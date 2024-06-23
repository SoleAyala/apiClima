import logging
import shutil
import pandas as pd
import os

# Obtener la instancia del logger configurado
logger = logging.getLogger('ApiClima')


def load_csv_to_db(file_path):
    from apiClima.app import db, Configuraciones

    # Leer el archivo CSV
    data = pd.read_csv(file_path)

    # Obtener el nombre del archivo sin la extensión
    table_name = "historico_hora_bulk_ID_" + os.path.splitext(os.path.basename(file_path))[0]
    print("Nombre de tabla: " + table_name)

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
    logger.info(f'Tabla {table_name} creada y datos insertados exitosamente.')
    print(f'Tabla {table_name} creada y datos insertados exitosamente.')

    #Carga de fecha Bulk en Tabla distritos


    # Mover el archivo a la carpeta de procesados
    processed_folder = db.session.query(Configuraciones).filter_by(parametro='path_bulk_procesados').first().valor
    print("El valor de la ruta procesados es: " + processed_folder)

    try:
        if not os.path.exists(processed_folder):
            os.makedirs(processed_folder)
        shutil.move(file_path, os.path.join(processed_folder, os.path.basename(file_path)))
        logger.info(f'Archivo {file_path} movido a la carpeta de procesados.')
        print(f'Archivo {file_path} movido a la carpeta de procesados.')
    except Exception as e:
        logging.error(f"Error moviendo el archivo a {processed_folder}: {e}")
