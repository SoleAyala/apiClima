import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup_logger():
    # Crea un logger
    logger = logging.getLogger('ApiClima')
    logger.setLevel(logging.INFO)  # Ajusta esto a tu necesidad, por ejemplo, DEBUG, ERROR, etc.
    # Define el path donde quieres guardar los logs
    log_directory = os.path.join(os.path.expanduser("~"), 'Desktop', 'api_clima_logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Crea un file handler que guarda los logs diariamente
    log_file = os.path.join(log_directory, 'app.log')
    handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1)
    handler.suffix = "%Y-%m-%d"  # Configura el formato de fecha del archivo de log

    # Crea un formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Añade el handler al logger
    logger.addHandler(handler)

    return logger


# Configura el logger
logger = setup_logger()
