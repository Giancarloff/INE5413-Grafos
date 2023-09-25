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
    
    def __repr__(self) -> str:
        return f"({self.__num}, {self.__label})"

class Grafo:
    '''
    Grafo não-dirigido e ponderado \n
    NOTA: Métodos de consulta que recebem vértices como parâmetros esperam:
        Objeto(s) do tipo Vértice XOR índice (começando em 1, corrigido dentro dos metodos)
    '''

    def __init__(self, vertices: fset[Vertice], edges: fset[fset[Vertice]], weights: dict) -> None:
        self.__vertices = vertices
        self.__edges = edges
        self.__weights = weights

        # Para termos O(1) lá teremos O(n) aqui
        self.__len_vertices = len(self.__vertices)
        self.__len_edges = len(self.__edges)

        default_list_range = range(self.__len_vertices)

        self.__grau = list(default_list_range)
        for v in self.__vertices:
            self.__grau[v.num - 1] = sum([1 for e in self.__edges if v in e])

        self.__rotulo = list(default_list_range)
        for v in self.__vertices:
            self.__rotulo[v.num - 1] = v.label

        # Representações
        self.__neighbours = list(default_list_range)
        self.__matrix = [[0]*self.__len_vertices]*self.__len_vertices

        for v in self.__vertices:
            neighbours = list()
            for u in self.__vertices:
                if fset([v.num, u.num]) in self.__edges:
                    pair = (u.num, self.__weights[fset([u.num,v.num])])
                    neighbours.append(pair)
            self.__neighbours[v.num - 1] = neighbours
        
        for v in self.__vertices:
            for u in self.__vertices:
                if fset([u, v]) in self.__edges:
                    self.__matrix[v.num - 1][u.num - 1] = self.__weights[fset([u, v])]
                else:
                    self.__matrix[v.num - 1][u.num - 1] = float('inf')

    # Debugging
    def __repr__(self) -> str:
        return f"".join(str(v) + " " for v in self.__vertices).join(str(e) + " " for e in self.__edges)

    @property
    def matrix(self):
        return self.__matrix
    
    @property
    def adj_list(self):
        return self.__neighbours

    def qtd_vertices(self) -> int: #O(1)
        return self.__len_vertices
    
    def qtd_arestas(self) -> int: #O(1)
        return self.__len_edges
    
    def grau(self, v) -> int: #O(1), assumindo O(isinstace) = O(1)
        if isinstance(v, int):
            return self.__grau[v - 1]
        elif isinstance(v, Vertice):
            return self.__grau[v.num - 1]
        else:
            raise ValueError
    
    def rotulo(self, v) -> str: #O(1), assumindo O(isinstace) = O(1)
        if isinstance(v, int):
            return self.__rotulo[v - 1]
        elif isinstance(v, Vertice):
            return self.__rotulo[v.num - 1]
        else:
            raise ValueError
    
    def vizinhos(self, v) -> list: #O(1)
        if isinstance(v, int):
            return self.__neighbours[v - 1]
        elif isinstance(v, Vertice):
            return self.__neighbours[v.num - 1]
        else:
            raise ValueError
    
    def ha_aresta(self, u, v) -> bool: #O(1), assumindo O(isinstace) = O(1)
        if isinstance(u, int) and isinstance(v, int):
            return self.__matrix[u - 1][v - 1] != 0
        elif isinstance(u, Vertice) and isinstance(v, Vertice):
            return self.__matrix[u.num - 1][v.num - 1] != 0
        else:
            raise ValueError

    def peso(self, u, v) -> float: #O(1), assumindo O(isinstace) = O(1)
        if isinstance(u, int) and isinstance(v, int):
            return self.__matrix[u - 1][v - 1]
        elif isinstance(u, Vertice) and isinstance(v, Vertice):
            return self.__matrix[u.num - 1][v.num - 1]
        else:
            raise ValueError

    # 2 [Buscas]
    def busca_largura(self, indice):
        '''
        NOTA: As estruturas de dados internaos operam
        sobre os índices corrigidos, exceto a fila
        que armazena os indices originais
        '''
        size_V = self.qtd_vertices()
        C = [False]*size_V
        D = [float('inf')]*size_V
        A = [None]*size_V
        
        # Vértice de origme
        C[indice - 1] = True
        D[indice - 1] = 0

        # Fila de visitas
        Q = list()
        Q.append(indice)

        while len(Q) > 0:
            I = Q.pop(0)
            for V, _ in self.vizinhos(I):
                if not C[V - 1]:
                    C[V - 1] = True
                    D[V - 1] = D[I - 1] + 1
                    A[V - 1] = I
                    Q.append(V)

        for d in set(D):
            print(f"{d}: ", end = "")
            for i, p in enumerate(D):
                if p == d:
                    print(f"{i + 1} ", end = "")
            print()

    # 3 [Ciclo Euleriano]
    def ciclo_euleriano(self):
        V: Vertice = None
        for v in self.__vertices:
            if self.grau(v) % 2 != 0:
                print(f"Vértice {v} com grau ímpar, não há ciclo euleriano.")
                break
            V = v if len(self.vizinhos(v)) != 0 else V
        
        # Usando Hierholzer
        C = [False]*self.qtd_arestas()
        E = enumerate(self.__edges)
        r, ciclo = self.__subciclo_euleriano(V, C, E)

        if not r: return (r, None)
        else:
            for i, _ in E:
                if not C[i]: return (C[i], None)
            
            return (True, ciclo)
        
    def __subciclo_euleriano(self, v: Vertice, C: list[bool], E: list) -> (bool, tuple):
        ciclo = list()
        ciclo.append(v)
        T: Vertice = v
        VU: fset = None

        while True:
            p = 0
            for i, e in E:
                if not C[i]: return (False, None)
                p += 1
                VU = e
            
            C[p] = True
            v = list(VU.difference(fset([v])))[0]

            ciclo.append(v)

            if T == v: break
        
        for i, e in E:
            if not C[i]:
                r: bool = None
                ciclo2: list = None
                X: Vertice = None
                for x in e:
                    X = x
                    r, ciclo2 = self.__subciclo_euleriano(x, C, E)
                    break

                if not r: return (False, None)
                
                if ciclo2.count(X) == 2:
                    where_to = ciclo.index(X)
                    ciclo.remove(X)
                    for p in ciclo2:
                        ciclo.insert(where_to + 1, p)

        return (True, ciclo)

    # 4 [Bellman-Ford ou Dijkstra]
    def bellman_ford(self, origem) -> (bool, list, list):
        if (isinstance(origem, Vertice)):
            origem = origem.num

        D = [float('inf')]*self.qtd_vertices()
        A = [None]*self.qtd_vertices()
        D[origem - 1] = 0

        for i in range(1, self.qtd_vertices() - 1):
            for e in self.__edges:
                u, v = e
                if D[v - 1] > D[u - 1] + self.__weights[e]:
                    D[v - 1] = D[u - 1] + self.__weights[e]
                    A[v - 1] = u

        for e in self.__edges:
            u, v = e
            if D[v - 1] > D[u - 1] + self.__weights[e]:
                self.__bellman_ford_print(False, D, A, origem=origem)
                return (False, None, None)
                
            
        self.__bellman_ford_print(True, D, A, origem=origem)
        return (True, D, A)
    
    def __bellman_ford_print(self, found, D, A, origem):
        if not found:
            print("Menor caminho not found.")

        for v in self.__vertices:
            d = 0
            if v.num == origem:
                print(f"{v.num}: {origem}; d = {d}")
            else:
                next_vertice = A[v.num]
                cost = 0
                A_list = list()
                A_list.append(v)
                while v != origem:
                    d += self.__weights(fset([v, next_vertice]))
                    v = next_vertice
                    next_vertice = A[v.num]
                print(f"{v.num}: ".join(str(u.num) + " " for u in self.__vertices if u == A[v.num - 1]))

def ler(file_name: str) -> Grafo:

    '''
    NOTA: Se o formato do arquivo não for exatamente
    o explícito no final do enunciado da atividade,
    o método não funciona.\n
    NOTA: Os arcos usam os índices dos vértices, não objetos do tipo vértice.
    '''

    # If it is .net
    if file_name[-4:] == ".net":
        with open(file=file_name, mode='r') as file:
            num_vertices = 0
            vertices = list()
            edges = list()
            weights = dict()

            comment_line = file.readline().split()

            if comment_line[0] == "*vertices":
                num_vertices = int(comment_line[1])
            else:
                print(f".net file in wrong format! Was expecting *vertices, got {comment_line[0]}")

            for _ in range(num_vertices):
                this_line = file.readline().split()
                index = int(this_line[0])
                label = "".join(word + " " for word in this_line[1:])
                vertices.append(Vertice(label, int(index)))

            comment_line = file.readline().strip()
            check = comment_line == "*edges" or comment_line == "*arcs"
            if check:
                while True:
                    this_line = file.readline().split()
                    if len(this_line) == 0: break

                    x = int(this_line[0])
                    y = int(this_line[1])
                    w = float(this_line[2])
                    new_edge = fset([x, y])
                    edges.append(new_edge)
                    weights[new_edge] = w

            else:
                print(f".net file in wrong format! Was expecting *edges or *arcs, got {comment_line}")

            return Grafo(fset(vertices), fset(edges), weights)
        # with open
    else:
        print("Arquivo de tipo desconhecido.")
        return None

