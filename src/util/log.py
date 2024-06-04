from logging.handlers import TimedRotatingFileHandler
import logging

def setup_logger(app):
    handler = TimedRotatingFileHandler(
        'app.log',
        when='midnight',
        interval=1,
        backupCount=150 # Se mantiene un backup del log de los últimos 150 días
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    handler.suffix = "%Y-%m-%d"

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
