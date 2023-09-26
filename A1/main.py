from grafos import Grafo, ler, mprint

caminho_minimo = "instancias/caminho_minimo/fln_pequena.net"
contem_ciclo_euleriano = "instancias/ciclo_euleriano/ContemCicloEuleriano.net"
sem_ciclo_euleriano = "instancias/ciclo_euleriano/SemCicloEuleriano.net"
facebook_santiago = "instancias/facebook/facebook_santiago.net"

file = contem_ciclo_euleriano 

print("Crindo Grafo...")
G = ler(file)
print(f"Grafo criado! Arquivo lido: {file}")

print("# Busca em Largura #")
G.busca_largura(1)

print("# Ciclo Euleriano")
print(G.ciclo_euleriano())

print("# Bellman-Ford")
G.bellman_ford(1)

print("# Floyd-Warshall")
G.floyd_warshall()