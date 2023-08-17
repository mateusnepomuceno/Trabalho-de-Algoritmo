import pandas as pd
import math


file_path = 'C:/Users/Mateus Nepomuceno/Documents/GitHub/Trabalho-de-Algoritmo/cidades_rn_2022 (1).xlsx'
df = pd.read_excel(file_path)

print(df)

#Encontrar distância entre as cidades do RN
between_cities = {}

for i in range(len(df)):
    city_1 = df.loc[i, 'CIDADE']
    lat1 = math.radians(df.loc[i, 'LAT'])
    lon1 = math.radians(df.loc[i, 'LONG'])

    for j in range(i+1, len(df)):
        city_2 = df.loc[j, 'CIDADE']
        lat2 = math.radians(df.loc[j, 'LAT'])
        lon2 = math.radians(df.loc[j, 'LONG'])

        dist_lon = lon2 - lon1
        dis_lat = lat2 - lat1

        between_cities_value = math.sin(dis_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dist_lon/2)**2

        # Evitar que o valor fique fora do intervalo permitido para a função atan2
        between_cities_value = min(1, int(between_cities_value))
        between_cities_value = max(-1, between_cities_value)

        angle_dist = 2 * math.atan2(math.sqrt(between_cities_value), math.sqrt(1 - between_cities_value))
        R = 6371  # Raio médio da Terra em quilômetros
        cal_dist = R * angle_dist

        if city_1 not in between_cities:
            between_cities[city_1] = {}
        if city_2 not in between_cities:
            between_cities[city_2] = {}

        between_cities[city_1][city_2] = cal_dist
        between_cities[city_2][city_1] = cal_dist