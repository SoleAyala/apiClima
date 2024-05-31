import pandas as pd


directionXml = 'ruta/a/tu/archivo.xls'

# Cargar el archivo XLS
df = pd.read_excel(directionXml, engine='openpyxl')

# Mostrar nombres de las columnas
print(df.head())

# Acceder a una columna específica
columnaEspecifica = df['nombre_columna']

# Mostrar la columna
print(columnaEspecifica)
