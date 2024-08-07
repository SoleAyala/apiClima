


def rebuild_dynamic_models():
    from sqlalchemy import inspect
    from app import db, dynamic_models, app
    with app.app_context():
        """Actualiza el registro de tablas existentes en la base de datos."""
        engine = db.engine
        inspector = inspect(engine)
        existing_tables = set(inspector.get_table_names())  # Obtener todas las tablas existentes

        # Filtrar solo las tablas que nos interesan
        dynamic_tables = {name for name in existing_tables if name.startswith('historico_hora_api_clima_')}
        # Actualizar el diccionario global con las tablas existentes
        dynamic_models.update((name, None) for name in dynamic_tables if name not in dynamic_models)