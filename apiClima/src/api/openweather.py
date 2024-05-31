import datetime
import requests
from zoneinfo import ZoneInfo  # Manejo de zonas horarias

from apiClima.src.util.time import timestampToDate


def clima_actual(lat, lon, api_key, exclude):
    url = "https://api.openweathermap.org/data/3.0/onecall"
    parameters = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  # Celsius
        'lang': 'es',  # Español
        'exclude': exclude
    }

    response = requests.get(url, params=parameters)
    data = response.json()

    # Obtención de los datos de la sección 'daily'
    daily_data = data['daily']

    fecha: str
    salida_sol: str
    puesta_sol: str
    salida_luna: str
    puesta_luna: str
    fase_lunar: str
    temp_maxima: str
    temp_minima: str
    temp_mañana: str
    temp_diurna: str
    temp_tarde: str
    temp_nocturna: str
    sensacion_mañana: str
    sensacion_diurna: str
    sensacion_tarde: str
    sensacion_nocturna: str
    presion_atmosferica: str
    humedad: str
    punto_rocio: str
    velocidad_viento: str
    rafagas_viento: str
    direccion_viento: str
    descripcion_clima: str
    nubosidad: str
    prob_precipitacion: str
    volumen_lluvia: str
    volumen_nieve: str
    indice_uv: str

    # Datos de los 8 días, el primer día es el día actual
    for day in daily_data:
        fecha = timestampToDate(day['dt'], day['timezone'])
        salida_sol = day['sunrise']
        puesta_sol = day['sunset']
        salida_luna = day.get('moonrise', 'No disponible')
        puesta_luna = day.get('moonset', 'No disponible')
        fase_lunar = day.get('moon_phase', 'No disponible')
        temp_maxima = day['temp']['max']
        temp_minima = day['temp']['min']
        temp_mañana = day['temp']['morn']
        temp_diurna = day['temp']['day']
        temp_tarde = day['temp']['eve']
        temp_nocturna = day['temp']['night']
        sensacion_mañana = day['feels_like']['morn']
        sensacion_diurna = day['feels_like']['day']
        sensacion_tarde = day['feels_like']['eve']
        sensacion_nocturna = day['feels_like']['night']
        presion_atmosferica = day['pressure']
        humedad = day['humidity']
        punto_rocio = day['dew_point']
        velocidad_viento = day['wind_speed']
        rafagas_viento = day.get('wind_gust', 0)
        direccion_viento = day['wind_deg']
        descripcion_clima = day['weather'][0]['description']
        nubosidad = day['clouds']
        prob_precipitacion = day['pop']
        volumen_lluvia = day.get('rain', 0)
        volumen_nieve = day.get('snow', 0)
        indice_uv = day['uvi']

        # Mostrar los valores almacenados
        print(f"Fecha (timestamp): {fecha}")
        print(f"Salida del sol (timestamp): {salida_sol}")
        print(f"Puesta del sol (timestamp): {puesta_sol}")
        print(f"Salida de la luna (timestamp): {salida_luna}")
        print(f"Puesta de la luna (timestamp): {puesta_luna}")
        print(f"Fase lunar: {fase_lunar}")
        print(f"Temperatura máxima: {temp_maxima} °C")
        print(f"Temperatura mínima: {temp_minima} °C")
        print(f"Temperatura de la mañana: {temp_mañana} °C")
        print(f"Temperatura diurna: {temp_diurna} °C")
        print(f"Temperatura de la tarde: {temp_tarde} °C")
        print(f"Temperatura nocturna: {temp_nocturna} °C")
        print(f"Sensación térmica de la mañana: {sensacion_mañana} °C")
        print(f"Sensación térmica diurna: {sensacion_diurna} °C")
        print(f"Sensación térmica de la tarde: {sensacion_tarde} °C")
        print(f"Sensación térmica nocturna: {sensacion_nocturna} °C")
        print(f"Presión atmosférica: {presion_atmosferica} hPa")
        print(f"Humedad: {humedad} %")
        print(f"Punto de rocío: {punto_rocio} °C")
        print(f"Velocidad del viento: {velocidad_viento} m/s")
        print(f"Ráfagas de viento: {rafagas_viento} m/s")
        print(f"Dirección del viento: {direccion_viento} grados")
        print(f"Descripción del clima: {descripcion_clima}")
        print(f"Nubosidad: {nubosidad} %")
        print(f"Probabilidad de precipitación: {prob_precipitacion * 100} %")
        print(f"Volumen de lluvia: {volumen_lluvia} mm")
        print(f"Volumen de nieve: {volumen_nieve} mm")
        print(f"Índice UV máximo del día: {indice_uv}")

    return data


# Substitute 'your_api_key' con tu clave API real
api_key = 'your_api_key'
latitude = 40.7128  # Ejemplo de latitud, cambia esto por la latitud real
longitude = -74.0060  # Ejemplo de longitud, cambia esto por la longitud real
exclude = 'current,minutely,hourly,alerts'  # Solo obtengo el daily

dato_clima_actual = clima_actual(latitude, longitude, api_key, exclude)
print(dato_clima_actual)

''' Ejemplo de la parte de la respuesta a usar, el daily =

"daily":[
    {
        "dt":1684951200,
        "sunrise":1684926645,
        "sunset":1684977332,
        "moonrise":1684941060,
        "moonset":1684905480,
        "moon_phase":0.16,
        "summary":"Expect a day of partly cloudy with rain",
        "temp":{
            "day":299.03,
            "min":290.69,
            "max":300.35,
            "night":291.45,
            "eve":297.51,
            "morn":292.55
        },
        "feels_like":{
            "day":299.21,
            "night":291.37,
            "eve":297.86,
            "morn":292.87
        },
        "pressure":1016,
        "humidity":59,
        "dew_point":290.48,
        "wind_speed":3.98,
        "wind_deg":76,
        "wind_gust":8.92,
        "weather":[
            {
                "id":500,
                "main":"Rain",
                "description":"light rain",
                "icon":"10d"
            }
        ],
        "clouds":92,
        "pop":0.47,
        "rain":0.15,
        "uvi":9.23
    },
    ...

'''
