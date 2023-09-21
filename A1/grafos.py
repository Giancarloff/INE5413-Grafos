class fset(frozenset): ...

class Vertice:

    def __init__(self, label: str, num: int) -> None:
        self.__label = label
        self.__num = num

    @property
    def num(self) -> int:
        return self.__num
    
    @property
    def label(self) -> int:
        return self.__label        

class Grafos:

    def __init__(self, vertices: fset[Vertice], edges: fset[fset[Vertice]], weights: dict) -> None:
        self.__vertices = vertices
        self.__edges = edges
        self.__weights = weights

        # O(1)
        self.__len_vertices = len(self.__vertices)
        self.__len_edges = len(self.__edges)

        # O(dict)
        self.__grau = dict()
        for v in self.__vertices:
            self.__grau[v] = sum([1 for e in self.__edges if v in e])

        self.__rotulo = dict()
        for v in self.__vertices:
            self.__rotulo[v] = v.label

        # Representações
        self.__matrix = list(range(self.__len_vertices))
        self.__neighbours = dict()

        self.__enum_vertices = enumerate(self.__vertices)

        for i, v in self.__enum_vertices:
            neighbours = [0]*self.__len_vertices
            for j, b in self.__enum_vertices:
                if fset(v, b) in self.__edges:
                    neighbours[j] = 1
            self.__matrix[i] = neighbours

        for v in self.__vertices:
            neighbours = list()
            for b in self.__vertices:
                if fset(v, b) in self.__edges:
                    neighbours.append(b)
            self.__neighbours[v] = neighbours


    def qtd_vertices(self) -> int: #O(1)
        return self.__len_vertices
    
    def qtd_arestas(self) -> int: #O(1)
        return self.__len_edges
    
    def grau(self, v) -> int: #O(dict)
        return self.__grau[v]
    
    def rotulo(self, v) -> str: #O(dict)
        return self.__rotulo[v]
    
    def vizinhos(self, v) -> list: #O(dict)
        return self.__neighbours[v]
    
    def ha_aresta(self, u, v) -> bool: #O(dict)
        return fset(u, v) in self.__edges

    #TODO melhorar abaixo
    def peso(self, u, v) -> float: 
        p = fset(u, v)
        return self.__weights[p] if p in self.__edges else float('inf')
    
    def ler():...
