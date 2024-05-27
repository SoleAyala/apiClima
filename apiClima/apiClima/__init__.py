from flask import Flask
from .extensions import db, migrate
from .blueprints.example_blueprint import example

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(example)

    return app
