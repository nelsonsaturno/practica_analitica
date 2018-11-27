import pandas as pd

# Datos de Accidentes de trafico en Madrid
df_accidents_2017 = pd.read_excel(
    'https://datos.madrid.es/egob/catalogo/300228-1-accidentes-trafico-detalle.xlsx'
)
df_accidents_2018 = pd.read_excel(
    'https://datos.madrid.es/egob/catalogo/300228-0-accidentes-trafico-detalle.xlsx'
)

# Nro. de accidentes en 2018 por distrito
df_accidents_by_district = df_accidents_2018.groupby(['DISTRITO'])['DISTRITO'].agg(['count']).reset_index()
print(df_accidents_by_district)

# Accidentes 2017-2018
df_all_accidents = pd.concat([df_accidents_2017, df_accidents_2018], sort=False).set_index('FECHA')
