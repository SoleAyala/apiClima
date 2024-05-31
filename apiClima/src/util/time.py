import datetime
from zoneinfo import ZoneInfo

def timestampToDate(timestamp, zona_horaria_paraguay):
    # Crear un objeto datetime en UTC con la zona horaria especificada
    fecha_hora_utc = datetime.datetime.fromtimestamp(timestamp, tz=ZoneInfo('UTC'))

    # Convertir de UTC a la zona horaria de Paraguay
    fecha_hora_paraguay = fecha_hora_utc.astimezone(zona_horaria_paraguay)
    fecha_paraguay = fecha_hora_paraguay.strftime('%Y-%m-%d')

    print("Fecha y hora en Paraguay:", fecha_hora_paraguay)

    return fecha_paraguay
