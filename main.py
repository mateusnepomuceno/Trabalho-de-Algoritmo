from tkinter import *
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

#classe para calcular a distância entre as cidades
class DistancesCalculator:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.R = 6373.0
        self.dist_entre_cid = {}
        self.calculate_distances()

    #percorre todas as cidades no dataframe
    def calculate_distances(self):
        for i in range(len(self.df)):
            cidade1 = self.df.loc[i, 'CIDADE']
            lat1 = radians(self.df.loc[i, 'LAT'])
            lon1 = radians(self.df.loc[i, 'LONG'])
            
            #calcula distâncias em relação a outras cidades
            for j in range(i + 1, len(self.df)):
                cidade2 = self.df.loc[j, 'CIDADE']
                lat2 = radians(self.df.loc[j, 'LAT'])
                lon2 = radians(self.df.loc[j, 'LONG'])

                dist_lon = lon2 - lon1
                dist_lat = lat2 - lat1

                valor_dist_entre_cid = sin(dist_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dist_lon / 2) ** 2
                dist_angu = 2 * atan2(sqrt(valor_dist_entre_cid), sqrt(1 - valor_dist_entre_cid))
                distancia_cal = self.R * dist_angu
                distancia_cal = round(distancia_cal, 2)

                #armazena a distância entre as cidades no dicionário
                if cidade1 not in self.dist_entre_cid:
                    self.dist_entre_cid[cidade1] = {}
                if cidade2 not in self.dist_entre_cid:
                    self.dist_entre_cid[cidade2] = {}

                self.dist_entre_cid[cidade1][cidade2] = distancia_cal
                self.dist_entre_cid[cidade2][cidade1] = distancia_cal

#classe para construção do grafo
class Grafo:
    def __init__(self, distances_calculator):
        self.distances_calculator = distances_calculator
        self.grafo = {}
        self.kruskal()

    def kruskal(self):
        #percorre todas as cidades
        for cidade in self.distances_calculator.dist_entre_cid:
            self.grafo[cidade] = set()
            #percorre os vizinhos de cada cidade
            for vizinhos in self.distances_calculator.dist_entre_cid[cidade]:
                if self.distances_calculator.dist_entre_cid[cidade][vizinhos] != 0:
                    peso = self.distances_calculator.dist_entre_cid[cidade][vizinhos]
                    aresta = (vizinhos, peso)
                    self.grafo[cidade].add(aresta)

#classe para encontrar a árvore geradora mínima usando Kruskal
class Arvore_ger_min:
    def __init__(self, graph_builder):
        self.graph_builder = graph_builder
        self.arvore_ger_min = []
        self.geradora()

    def geradora(self):
        arestas = []
        for cidade in self.graph_builder.grafo:
            for aresta in self.graph_builder.grafo[cidade]:
                arestas.append((aresta[1], cidade, aresta[0]))
        arestas.sort()

        pais = {}
        altura = {}
        for cidade in self.graph_builder.grafo:
            pais[cidade] = cidade
            altura[cidade] = 0

        #função para encontrar a raiz de um conjunto
        def encontrar(cidade):
            if pais[cidade] != cidade:
                pais[cidade] = encontrar(pais[cidade])
            return pais[cidade]

        #função para unir dois conjuntos
        def unir(cidade1, cidade2):
            raiz1 = encontrar(cidade1)
            raiz2 = encontrar(cidade2)
            if raiz1 != raiz2:
                if altura[raiz1] > altura[raiz2]:
                    pais[raiz2] = raiz1
                else:
                    pais[raiz1] = raiz2
                    if altura[raiz1] == altura[raiz2]:
                        altura[raiz2] += 1

        for aresta in arestas:
            peso, cidade1, cidade2 = aresta
            if encontrar(cidade1) != encontrar(cidade2):
                self.arvore_ger_min.append(aresta)
                unir(cidade1, cidade2)

#classe para a interface gráfica
class InterfaceGrafica:
    def __init__(self, minimum_spanning_tree):
        self.minimum_spanning_tree = minimum_spanning_tree
        self.janela = Tk()
        self.janela.title("Árvore Geradora Mínima")
        self.janela.geometry("600x400")
        self.frame_botoes = ttk.Frame(self.janela)
        self.frame_botoes.pack(side="top", fill="x")
        self.botao_menores = ttk.Button(self.frame_botoes, text="Menores Distâncias", command=self.mostrar_menores)
        self.botao_menores.pack(side="left", padx=5, pady=5)
        self.botao_maiores = ttk.Button(self.frame_botoes, text="Maiores Distâncias", command=self.mostrar_maiores)
        self.botao_maiores.pack(side="left", padx=5, pady=5)
        self.botao_Arvore_ger_min = ttk.Button(self.frame_botoes, text="Arvore_ger_min", command=self.Arvore_ger_min)
        self.botao_Arvore_ger_min.pack(side="left", padx=5, pady=5)
        self.treeview = ttk.Treeview(self.janela, columns=("Distância", "Origem", "Destino"))
        self.treeview.pack(side="top", fill="both", expand=True)
        self.treeview.heading("#0", text="ID")
        self.treeview.column("#0", width=0, stretch="no")
        self.treeview.heading("Distância", text="Distância")
        self.treeview.column("Distância", anchor="center", width=100)
        self.treeview.heading("Origem", text="Origem")
        self.treeview.column("Origem", anchor="center", width=100)
        self.treeview.heading("Destino", text="Destino")
        self.treeview.column("Destino", anchor="center", width=100)
        self.construir_interface()

    def construir_interface(self):
        self.botao_visualizar = ttk.Button(self.frame_botoes, text="gráfico da árvore", command=self.visualizar_arvore)
        self.botao_visualizar.pack(side="left", padx=5, pady=5)

    def visualizar_arvore(self):
        arvore_ger_min_grafo = nx.Graph()
        for aresta in self.minimum_spanning_tree.arvore_ger_min:
            arvore_ger_min_grafo.add_edge(aresta[1], aresta[2], peso=aresta[0])

        pos = nx.spring_layout(arvore_ger_min_grafo, k=0.5)
        nx.draw_networkx_edges(arvore_ger_min_grafo, pos, node_size=10)
        nx.draw_networkx_nodes(arvore_ger_min_grafo, pos, node_size=100, node_color='red', alpha=0.8)
        nx.draw_networkx_labels(arvore_ger_min_grafo, pos, font_size=7)
        plt.axis('off')
        plt.show()

    def mostrar_menores(self):
        arestas_ordenadas = sorted(self.minimum_spanning_tree.arvore_ger_min, key=lambda x: x[0])
        menores = arestas_ordenadas[:5]
        self.atualizar_tabela(menores)

    def mostrar_maiores(self):
        arestas_ordenadas = sorted(self.minimum_spanning_tree.arvore_ger_min, key=lambda x: x[0], reverse=True)
        maiores = arestas_ordenadas[:5]
        self.atualizar_tabela(maiores)

    def Arvore_ger_min(self):
        self.atualizar_tabela(self.minimum_spanning_tree.arvore_ger_min)

    def atualizar_tabela(self, items):
        for child in self.treeview.get_children():
            self.treeview.delete(child)
        for item in items:
            distancia_formatada = f"{round(item[0], 2)} km"
            self.treeview.insert("", "end", values=(distancia_formatada, item[1], item[2]))

class MainApp:
    def __init__(self, file_path):
        distances_calculator = DistancesCalculator(file_path)
        graph_builder = Grafo(distances_calculator)
        minimum_spanning_tree = Arvore_ger_min(graph_builder)
        interface_grafica = InterfaceGrafica(minimum_spanning_tree)

        interface_grafica.janela.mainloop()


file_path = r'cidades_rn_2022 (1).xlsx'
app = MainApp(file_path)

