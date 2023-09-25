from grafos import Grafo, ler

caminho_minimo = "instancias/caminho_minimo/fln_pequena.net"
contem_ciclo_euleriano = "instancias/ciclo_euleriano/ContemCicloEuleriano.net"
sem_ciclo_euleriano = "instancias/ciclo_euleriano/SemCicloEuleriano.net"

file = contem_ciclo_euleriano

G = ler(file)
print(f"Arquivo lido: {file}")

print("# Busca em Largura #")
G.busca_largura(1)

print("# Ciclo Euleriano")
print(G.ciclo_euleriano())

print("Bellman-Ford")
print(G.bellman_ford(1))