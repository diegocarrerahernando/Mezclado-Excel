import pandas as pd
from difflib import SequenceMatcher

# Ruta de los archivos de entrada y salida
archivo = 'C:/Users/TI/Documents/Volcado BBDD/BBDD Agrupadas.xlsx'
archivo_salida = 'C:/Users/TI/Documents/Volcado BBDD/BBDD Final.xlsx'

# Cargar archivos Excel en DataFrames
df_hubspot = pd.read_excel(archivo, sheet_name='Hubspot').fillna('')
df_automatricula = pd.read_excel(archivo, sheet_name='Automatrícula').fillna('')
df_automatricula.rename(columns={'Nombre': 'Nombre2'}, inplace=True)


# Función para calcular la similitud entre cadenas de texto
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


# Crear una lista para almacenar las filas del archivo de salida
filas_salida = []

ocurrencias = 0
indices_hubspot = []
indices_automatricula = []

# Iterar sobre las filas del primer archivo
for index1, fila1 in df_hubspot.iterrows():
    nombre1 = fila1['Nombre']
    apellido1_1 = fila1['Apellido 1']
    apellido2_1 = fila1['Apellido 2']
    correo1 = fila1['Correo']

    # Iterar sobre las filas del segundo archivo
    for index2, fila2 in df_automatricula.iterrows():
        nombre2 = fila2['Nombre2']
        apellido1_2 = fila2['1er apellido']
        apellido2_2 = fila2['2º apellido']
        correo2 = fila2['Email']

        # Comparar los campos de los nombres, apellidos y correos
        similitud_nombre = similar(str(nombre1), str(nombre2))
        similitud_apellido1 = similar(apellido1_1, apellido1_2)
        similitud_apellido2 = similar(apellido2_1, apellido2_2)
        if correo1 == '' and correo2 != '':
            similitud_correo = 1
        elif correo1 != '' and correo2 == '':
            similitud_correo = 1
        else:
            similitud_correo = similar(correo1, correo2)

        # Comprobar si se cumple el umbral de similitud
        if (similitud_nombre > 0.70 and similitud_apellido1 > 0.70 and similitud_apellido2 > 0.70 and
                similitud_correo > 0.70):
            indices_hubspot.append(index1)
            indices_automatricula.append(index2)
            ocurrencias += 1

            # Unir las filas con similitud alta en una sola fila
            fila_salida = pd.concat([fila1, fila2], axis=0)
            # fila_salida = fila1.append(fila2)
            filas_salida.append(fila_salida)

# Borrar las filas que coinciden en los DataFrames originales
df_hubspot = df_hubspot.drop(indices_hubspot, axis=0)
df_automatricula = df_automatricula.drop(indices_automatricula, axis=0)

# Crear un nuevo DataFrame con las filas de salida
df_salida = pd.concat(filas_salida, axis=1)
df_salida = df_salida.transpose()

# Mezclar los dos dataframes originales
df_salida = pd.concat([df_hubspot, df_salida, df_automatricula], axis=0, ignore_index=True).fillna('')

# Cambiar la ubicación de los valores de los campos de nombre y apellido de df_automatricula a su lugar correspondiente
# en df_salida (hecho sobre df_hubspot)
for indice, fila in df_salida.iterrows():
    if fila['Nombre2'] != '' and fila['Nombre'] == '':
        df_salida.loc[indice, 'Nombre'] = fila['Nombre2']
        df_salida.loc[indice, 'Apellido 1'] = fila['1er apellido']
        df_salida.loc[indice, 'Apellido 2'] = fila['2º apellido']

# Borrar las columnas que no hacen falta
df_salida = df_salida.drop(['Nombre2', '1er apellido', '2º apellido', 'Associated Deal.1', 'webinar.1',
                            'Associated Company.1', 'Associated Deal IDs.1'], axis=1)

# Guardar el DataFrame en un nuevo archivo Excel
df_salida.to_excel(archivo_salida, sheet_name='BBDD Agrupada', index=True)

print(ocurrencias)

