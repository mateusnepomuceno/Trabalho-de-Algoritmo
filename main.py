import pandas as pd
import math

file_path = 'C:/Users/Mateus Nepomuceno/Documents/GitHub/Trabalho-de-Algoritmo/cidades_rn_2022 (1).xlsx'
df = pd.read_excel(file_path)

# Encontrar distância entre as cidades do RN
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

        # Atualizar entre_cities_value sem conversão para int
        between_cities_value = min(1, between_cities_value)
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

# Criar o grafo a partir do dicionário between_cities
graph = {}

for city, neighbors in between_cities.items():
    graph[city] = set()
    for neighbor, distance in neighbors.items():
        graph[city].add((neighbor, distance))

# Algoritmo de Kruskal
def kruskal(graph):
    # Função para encontrar a raiz de um conjunto usando compressão de caminho
    def find(parents, vertex):
        if parents[vertex] != vertex:
            parents[vertex] = find(parents, parents[vertex])
        return parents[vertex]

    # Função para unir dois conjuntos
    def union(parents, ranks, vertex1, vertex2):
        root1 = find(parents, vertex1)
        root2 = find(parents, vertex2)

        if root1 != root2:
            if ranks[root1] < ranks[root2]:
                parents[root1] = root2
            else:
                parents[root2] = root1
                if ranks[root1] == ranks[root2]:
                    ranks[root1] += 1

    edges = []
    for vertex, neighbors in graph.items():
        for neighbor, weight in neighbors:
            edges.append((weight, vertex, neighbor))

    edges.sort()  # Ordena as arestas pelo peso (distância)

    minimum_spanning_tree = []
    parents = {vertex: vertex for vertex in graph}
    ranks = {vertex: 0 for vertex in graph}

    for weight, vertex1, vertex2 in edges:
        if find(parents, vertex1) != find(parents, vertex2):
            minimum_spanning_tree.append((vertex1, vertex2, weight))
            union(parents, ranks, vertex1, vertex2)

    return minimum_spanning_tree

# Executar o algoritmo de Kruskal no grafo
minimum_spanning_tree = kruskal(graph)

# Imprimir a árvore geradora mínima
for edge in minimum_spanning_tree:
    vertex1, vertex2, weight = edge
    print(f"City 1: {vertex1}, City 2: {vertex2}, Weight: {weight}")
