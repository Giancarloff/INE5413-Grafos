class fset(frozenset): ...

class Grafo:
    '''
    Grafo não-dirigido e ponderado \n
    NOTA: Métodos de consulta que recebem vértices como parâmetros esperam:
    '''

    def __init__(self, vertices: fset, edges: fset[fset], weights: dict) -> None:
        self.__edges = edges
        self.__weights = weights

        self.__vertices = [0]*len(vertices)
        self.__rotulo = [""]*len(vertices)

        for index, label in vertices:
            self.__vertices[index - 1] = index
            self.__rotulo[index - 1] = label

        # Para termos O(1) lá teremos O(n) aqui
        self.__len_vertices = len(self.__vertices)
        self.__len_edges = len(self.__edges)

        default_list_range = range(self.__len_vertices)

        self.__grau = list(default_list_range)
        for v in self.__vertices:
            self.__grau[v - 1] = sum([1 for e in self.__edges if v in e])

        # Representações
        self.__neighbours = list(default_list_range)
        self.__matrix = [[0]*self.__len_vertices]*self.__len_vertices

        for v in self.__vertices:
            neighbours = list()
            for u in self.__vertices:
                if fset([v, u]) in self.__edges:
                    pair = (u, self.__weights[fset([u, v])])
                    neighbours.append(pair)
            self.__neighbours[v - 1] = neighbours
        
        for v in self.__vertices:
            for u in self.__vertices:
                if fset([u, v]) in self.__edges:
                    self.__matrix[v - 1][u - 1] = self.__weights[fset([u, v])]
                else:
                    self.__matrix[v - 1][u - 1] = float('inf')

    # Debugging
    def __repr__(self) -> str:
        return f"".join(str(v) + " " for v in self.__vertices) + ";; " + "".join(str(e) + " " for e in self.__edges)

    @property
    def matrix(self):
        return self.__matrix
    
    @property
    def adj_list(self):
        return self.__neighbours
    
    @property
    def vertices(self):
        return self.__vertices

    @property
    def edges(self):
        return self.__edges

    @property
    def weights(self):
        return self.__weights

    def qtd_vertices(self) -> int: #O(1)
        return self.__len_vertices
    
    def qtd_arestas(self) -> int: #O(1)
        return self.__len_edges
    
    def grau(self, v) -> int: #O(1)
        return self.__grau[v - 1]
    
    def rotulo(self, v) -> str: #O(1)
        return self.__rotulo[v - 1]
    
    def vizinhos(self, v) -> list: #O(1)
        return self.__neighbours[v - 1]
    
    def ha_aresta(self, u, v) -> bool: #O(1)
        return self.__matrix[u - 1][v - 1] != 0

    def peso(self, u, v) -> float: #O(1)
        return self.__matrix[u - 1][v - 1]

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
        for v in self.vertices:
            if self.grau(v) % 2 != 0: 
                print("0")
                return None

        found = False
        path = list()
        visited = list()
        for v in self.__vertices:
            self.recursive_search(v, v, path, visited)
            found = all(e in visited for e in self.__edges)
            if found: 
                path.append(v)
                break
        
        # Printing
        if found:
            print("1")
            for i, n in enumerate(path):
                if i < len(path) - 1:
                    print(n, end = ", ")
                else:
                    print(n)
        else:
            print("0")
            print(None)

        return path if found else []

    def recursive_search(self, O, V, path: list, visited: list):
        '''
        Logicamente funciona sem a lista path, porém\n
        ela é necessária para o print
        '''
        for e in self.__edges:
            if e not in visited and V in e:
                path.append(V)
                visited.append(e)
                u, v = e
                N = u if u != V else v
                self.recursive_search(O, N, path, visited)

        all_edges = all(e in visited for e in self.__edges)
        if not all_edges and len(path) > 0:
            path.pop()

        # return path

    # 4 [Bellman-Ford ou Dijkstra]
    def bellman_ford(self, origem) -> (bool, list, list):
        D = [float('inf')]*self.qtd_vertices()
        A = [None]*self.qtd_vertices()
        D[origem - 1] = 0

        for _ in range(1, self.qtd_vertices() - 1):
            for e in self.__edges:
                u, v = e
                if D[v - 1] > D[u - 1] + self.__weights[e]:
                    D[v - 1] = D[u - 1] + self.__weights[e]
                    A[v - 1] = u
                elif D[u - 1] > D[v - 1] + self.__weights[e]:
                    D[u - 1] = D[v - 1] + self.__weights[e]
                    A[u - 1] = v

        for e in self.__edges:
            u, v = e
            if D[v - 1] > D[u - 1] + self.__weights[e]:
                self.__bellman_ford_print(False, A, origem=origem)
                return (False, None, None)
                
            
        self.__bellman_ford_print(True, A, origem=origem)
        return (True, D, A)
    
    def __bellman_ford_print(self, cycle_free, A, origem):
        if not cycle_free:
            print("Ciclo negativo encontrado.")
            return

        for v in self.__vertices:
            print(f"{v}: ", end = "")
            d = 0
            path = list()
            a = v
            if v == origem:
                print(f"{v}", end = "")
            else:
                while True:
                    if A[a - 1] is not None:
                        d += self.__weights[fset([a, A[a - 1]])]
                    path.append(a)
                    a = A[a - 1]
                    if a == origem or a is None:
                        path.append(a)
                        break
                
                for i, p in enumerate(reversed(path)):
                    if None in path: break
                    if i < len(path) - 1:
                        print(f"{p}, ", end = "")
                    else:
                        print(f"{p}", end = "")
                    
            print(f"; d = {d}")

    # 5 [Floyd-Warshall]
    def floyd_warshall(self):
        F = self.qtd_vertices()
        D = [[[0]*F for _ in range(F)] for _ in range(F)]
        D[0] = self.__W()

        for k in range(1, F):
            for v in self.__vertices:
                for u in self.__vertices:
                    S = D[k - 1][u - 1][k - 1] + D[k - 1][k - 1][v - 1]
                    D[k][v - 1][u - 1] = min([D[k - 1][v - 1][u - 1], S])

        self.__print_floyd_warshall(D[F-1])
        return D[F - 1]

    def __W(self) -> list:
        F = self.qtd_vertices()
        D = [[0]*F for _ in range(F)]

        for v in self.__vertices:
            for u in self.__vertices:
                e = fset({v, u})
                if e in self.__edges:
                    D[v - 1][u - 1] = self.__weights[e]
                elif v != u:
                    D[v - 1][u - 1] = float('inf')

        return D 

    def __print_floyd_warshall(self, D):
        for v in self.__vertices:
            print(f"{v}: ", end = "")
            for u in self.__vertices:
                print(f"{D[v - 1][u - 1]}, ", end = "")
            print()

class GrafoDirigido(Grafo):

    '''
    Classe para Grafos dirigidos e não-ponderados
    '''

    def __init__(self, vertices: fset, edges: fset[tuple], __weights) -> None:
        super().__init__(vertices, edges, __weights)

    def __repr__(self):
        return f"".join(str(v) + " " for v in self.vertices) + " ;; " + "".join(str(e) + " " for e in self.edges)

    # Override
    def peso(self, u, v):
        return self.weights[(u, v)]

    # Métodos úteis
    def vizinhos_positivos(self, v):
        pos_hood = list()
        for (p, q) in self.edges:
            if v == p: pos_hood.append(q)

        return pos_hood

    # 1. [Componentes Fortemente Conexas]
    def componentes_conexas(self):
        '''
        NOTA: Estruturas de dados retornadas têm indice corrigido! (por -1), ou seja,
        não pode-se acessar o dado passando o vértice v original, deve-se passar v - 1
        '''
        _, _, _, F = self.__dfs()

        ET_list = list()
        for (u, v) in self.edges:
            ET_list.append((v, u))
        
        ET = fset(ET_list)

        vlist = list()
        for v in self.vertices:
            vlist.append((v, self.rotulo(v)))

        GT = GrafoDirigido(fset(vlist), ET, self.weights)

        _, _, A2, _ = GT.dfs_adaptado(F)

        self.__print_conexas(A2)

        return A2

    def __dfs(self):
        '''
        NOTA: Estruturas de dados retornadas têm indice corrigido! (por -1)
        '''
        qtd_v = self.qtd_vertices()
        C = [False]*qtd_v
        T = [float('inf')]*qtd_v
        F = [float('inf')]*qtd_v
        A = [None]*qtd_v

        tempo = 0

        for v in self.vertices:
            if not C[v - 1]:
                self.__dfs_visit(v, C, T, A, F, tempo)

        return C, T, A, F

    def dfs_adaptado(self, F):
        '''
        NOTA: Estruturas de dados retornadas têm indice corrigido! (por -1)
        '''
        qtd_v = self.qtd_vertices()
        C = [False]*qtd_v
        T = [float('inf')]*qtd_v
        F2 = [float('inf')]*qtd_v
        A = [None]*qtd_v

        tempo = 0

        for v, _ in sorted(enumerate(self.vertices), key=lambda x: x[1], reverse=True):
            # Sort dos vértices pelo segundo elemento (tempo de F = x[1]) da enumeração, revertido pra ter-se do maior pro menor
            if not C[v - 1]:
                self.__dfs_visit(v, C, T, A, F, tempo)

        return C, T, A, F2

    def __dfs_visit(self, v, C, T, A, F, tempo):
        C[v - 1] = True
        tempo += 1
        T[v - 1] = tempo

        for u in self.vizinhos_positivos(v):
            A[u - 1] = v
            self.__dfs_visit(u, C, T, A, F, tempo)

        tempo += 1
        F[v - 1] = tempo

    def __print_conexas(self, A):
        S = dict()
        for v in self.vertices:
            S[v] = list([v])
        
        for v in self.vertices:
            if A[v - 1] is not None:
                x = list()
                x.extend(S[v])
                x.extend(S[A[v - 1]])

                for y in x:
                    S[y] = x

        S_list = list()
        for key in S.keys():
            X = S[key]
            if X not in S_list:
                S_list.append(S[key])

        for l in S_list:
            print("".join(str(q) + "," for q in l[:-1]), end="")
            print(l[-1])


    # 2. [Ordenação Topológica]
    def ordenacao_topologica(self):
        '''
        Não há verificação de ciclos no Grafo - espera-se input nos conformes
        '''

        len_v = self.qtd_vertices()
        C = [False]*len_v
        T = [float('inf')]*len_v
        F = [float('inf')]*len_v

        tempo = 0

        O = list()
        for v in self.vertices:
            if not C[v - 1]:
                self.__dfs_visit_ot(v, C, T, F, tempo, O)

        # Print
        for v in O[:-1]:
            print(self.rotulo(v), end=" → ")

        print(self.rotulo(O[-1]), end=". \n")

        return O
    
    def __dfs_visit_ot(self, v, C, T, F, tempo, O: list):
        C[v - 1] = True
        tempo += 1
        T[v - 1] = tempo

        for u in self.vizinhos_positivos(v):
            if not C[u - 1]:
                self.__dfs_visit_ot(u, C, T, F, tempo, O)
        
        tempo += 1
        F[v - 1] = tempo

        O.insert(0, v)

    # 3. [Kruskal ou Prim]
    # Kruskal
    def arvore_minima_geradora(self):
        A = list()
        S = dict()

        for v in self.vertices:
            S[v] = list()
            S[v].append(v)

        # Lista de (aresta, peso)
        Ep = list()
        for (u, v) in self.edges:
            Ep.append(((u, v), self.peso(u, v)))

        Ep.sort(key = lambda x: x[1]) # Sort crescente por pesos
        # key aplica a função e faz o sort pelos resultados

        for (u, v), _ in Ep:
            if S[u] != S[v]:
                A.append((u, v))
                x = list()
                x.extend(S[u])
                x.extend(S[v])

                for y in x:
                    S[y] = x

        # Print
        print(sum(self.peso(u, v) for u, v in A))
        for (p, q) in A[:-1]:
            print(f"{p}-{q}", end=", ")
        print(f"{A[-1][0]}-{A[-1][1]}")

        return A

def mprint(list):
    for n in list:
        print(n) 

def ler(file_name: str, dirigido: bool = False) -> Grafo | GrafoDirigido:

    '''
    NOTA: Se o formato do arquivo não for exatamente
    o explícito no final do enunciado da atividade,
    o método não funciona.\n
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
                vertices.append((int(index), label))

            comment_line = file.readline().strip()

            if comment_line != "*edges" and comment_line != "*arcs":
                print(f".net file in wrong format! Was expecting *edges or *arcs, got {comment_line}")
                return None
            
            if not dirigido:
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
                while True:
                    this_line = file.readline().split()
                    if (len(this_line) == 0): break

                    x = int(this_line[0])
                    y = int(this_line[1])
                    w = float(this_line[2])

                    new_edge = tuple([x, y])
                    edges.append(new_edge)
                    weights[new_edge] = w

            return Grafo(fset(vertices), fset(edges), weights) if not dirigido else GrafoDirigido(fset(vertices), fset(edges), weights)
        # with open
    else:
        print("Arquivo de tipo desconhecido.")
        return None

