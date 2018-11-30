import pandas as pd
import matplotlib.pyplot as plt

# Se cargan los datos y se renombran todas las columnas
new_names = [
    'fecha', 'rango_horario', 'dia_semana', 'distrito',
    'lugar_accidente', 'num_calle', 'num_parte', 'fa_granizo',
    'fa_hielo', 'fa_lluvia', 'fa_niebla', 'fa_seco', 'fa_nieve',
    'sv_mojado', 'sv_aceite', 'sv_barro', 'sv_grava_suelta',
    'sv_hielo', 'sv_seca_limpia', 'num_victimas', 'tipo_accidente',
    'tipo_vehiculo', 'tipo_persona', 'sexo', 'lesividad', 'tramo_edad'
]

# Datos para 2017
df_accidents_2017 = pd.read_excel(
    'https://datos.madrid.es/egob/catalogo/300228-1-accidentes-trafico-detalle.xlsx',
    skiprows=0, names=new_names
)

# Datos para 2018
df_accidents_2018 = pd.read_excel(
    'https://datos.madrid.es/egob/catalogo/300228-0-accidentes-trafico-detalle.xlsx',
    skiprows=0, names=new_names
)

# Unión de datos 2017-2018
df_all_accidents = pd.concat([df_accidents_2017, df_accidents_2018], sort=False)

# Victimas por accidente
s_num_victims_by_accident = df_all_accidents.groupby(['num_parte'])['num_victimas'].sum()

# Accidentes donde no existe ningún factor climático
df_best_weather = df_all_accidents[
    (df_all_accidents['sv_seca_limpia'] == 'SI') & (df_all_accidents['fa_seco'] == 'SI')
]

# Accidentes en días laborables
weekdays = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES']

df_accidents_on_weekdays = df_all_accidents[df_all_accidents['dia_semana'].isin(weekdays)]

# Accidentes por distrito y por anio
df_accidents_by_district = pd.pivot_table(
    df_all_accidents, index=['distrito'], columns=[df_all_accidents['fecha'].dt.year],
    aggfunc=pd.Series.nunique, values='num_parte'
)

# Se verifica que el resultado es correcto
if not df_accidents_by_district[2017].sum() == df_accidents_2017['num_parte'].nunique():
    raise Exception("Error para el año 2017")
if not df_accidents_by_district[2018].sum() == df_accidents_2018['num_parte'].nunique():
    raise Exception("Error para el año 2018")


# Renombramiento de valores de la columna 'lesividad' en una nueva columna
def readable_injury(key):
    injury = {
        'IL': 'ILESO',
        'HL': 'HERIDO LEVE',
        'HG': 'HERIDO GRAVE',
        'MT': 'MUERTO'
    }
    return injury.setdefault(key, 'NO ASIGNADA')


df_all_accidents['tipo_lesividad'] = df_all_accidents['lesividad'].apply(readable_injury)

# Número de personas por tipo de lesividad calculado por año
df_injuries_by_year = pd.pivot_table(
    df_all_accidents, index=['tipo_lesividad'], columns=[df_all_accidents['fecha'].dt.year],
    aggfunc='sum', values='num_victimas'
)

if not df_accidents_2017['num_victimas'].sum() == df_injuries_by_year[2017].sum():
    raise Exception("Error para el año 2017")
if not df_accidents_2018['num_victimas'].sum() == df_injuries_by_year[2018].sum():
    raise Exception("Error para el año 2018")

