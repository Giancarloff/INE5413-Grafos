from numpy import Infinity as INF

'''
TODO:
    Fix vertices not being their indexes for the lists (maybe a true_index list or the sorts)
    Fix file reader (check facebook test)
    Find more O(1) algorithms for the methods
'''

class Grafo_no_p:
    
    def __init__(self, vertices: frozenset | set, arestas: frozenset | set, pesos: dict, rotulos: list) -> None:
        '''
        Notas:
        - Se não forem dados vértices um conjunto vazio é usado
        - Idem para arestas, e espera-se que as arestas sejam sets de sets (representação {u, v} para u,v em vertices)
        - Espera-se peso['{u, v}'] = X para X float
        - pesos não definidos por parâmetro são definidos no construtor como numpy.Infinity
        - Essa implementação prevê que não haverão operações de inserção de vértices e arestas
        '''
        
        self.__vertices = vertices if vertices != None else frozenset()
        self.__edges = arestas if arestas != None else frozenset()
        self.__weights = pesos if pesos != None else dict()
        self.__label_of = rotulos if rotulos != None else dict()

        # Preciso de tipos hashaveis
        if isinstance(self.__vertices, set):
            self.__vertices = frozenset(self.__vertices)

        if isinstance(self.__edges, set):
            self.__edges = frozenset(self.__edges)

        if self.__vertices.issubset({}):
            print("Conjunto de vertices vazio")
            return
        elif self.__edges.issubset({}):
            print("Conjunto de arestas vazia.")
            return
        elif set(self.__weights.keys()).issubset({}):
            print("Função de pesos vazia.")
            return
        elif len(self.__label_of) != len(self.__vertices):
            print(f"Rotulação mal formulada: Num vertices = {len(self.__vertices)} Num rotulos = {len(self.__label_of)}")
            return

        # Verificando se as arestas estão bem formadas
        for e in self.__edges:
            if len(e) != 2:
                print(f"Aresta mal formada: {str(e)}")
                return
            else:
                if not all(t in self.__vertices for t in e):
                    print(f"Aresta com vértice desconhecida: {str(e)}; Vertices: {self.__vertices}")
                    return
                
        # Tudo verificado, completando pesos
        weight_undefined = arestas.difference(frozenset(pesos.keys()))
        for e in weight_undefined:
            self.__weights[e] = INF # INF = numpy.Infinity (float)

        # Para complexidade O(1) em qtdVertices, qtdArestas
        self.__num_vertices = len(vertices)
        self.__num_edges = len(arestas)

        self.__degree_of = list()
        self.__neighbors_of = list()
        vertices_sorted = list(self.__vertices).sort()
        for v in vertices_sorted:
            # Para complexidade O(1) em grau(v)
            # Os appends assumem que a lista de vertices está ordenada 
            count = 0
            for e in self.__edges:
                if v in e and self.__weights[e] != INF:
                    count += 1
            self.__degree_of.append(count)

            # Para complexidade O(1) em vizinhos(v)
            neighborhood = list()
            for e in self.__edges:
                if v in e:
                    neighborhood.append(e.difference(frozenset({v})))
            self.__neighbors_of.append(neighborhood)


    def qtdVertices(self) -> int:
        return self.__num_vertices
    
    def qtdArestas(self) -> int:
        return self.__num_edges
    
    def grau(self, v: int) -> int:
        return self.__degree_of[v]
    
    def rotulo(self, v: int) -> str:
        return self.__label_of[v]
    
    def vizinhos(self, v: int) -> list:
        return self.__neighbors_of[v]
    
    def haAresta(self, e: frozenset | set) -> bool:
        if isinstance(e, set):
            e = frozenset(e)
        return e in self.__edges # O(n)
        
    def peso(self, e: frozenset | set) -> float:
        if isinstance(e, set):
            e = frozenset(e)
        # Nota: Relembrar o construtor
        # Complexidade: O(n)
        return self.__weights[e]
        
    @classmethod
    def ler(arquivo: str) -> tuple[frozenset, frozenset, dict, list]:
        vertices = set()
        rotulos = list()
        arestas = set()
        pesos = dict()
        with open(arquivo) as file:
            this_line = file.readline()
            if "*vertices" in this_line:
                _, num_vertices = this_line.split(" ")
                for _ in range(num_vertices):
                    this_line = file.readline()
                    splitted = this_line.split(" ")
                    if len(splitted) != 2:
                        print(f"Linha mal formada: {this_line}")
                        return
                    else:
                        vertice, rotulo = splitted
                        vertices.add(int(vertice))
                        rotulos.append(rotulo)
                
                # Edges
                this_line = file.readline()
                if "*edges" == this_line:
                    this_line = file.readline()
                    while this_line != "": # Na pratica vai executar até EOF devido ao with open
                        splitted = this_line.split(" ")
                        if len(splitted) != 3:
                            print(f"Linha mal formada: {this_line}")
                        else:
                            a, b, peso = splitted
                            a, b, peso = int(a), int(b), float(peso)
                            aresta = frozenset({a, b})

                            arestas.add(frozenset({a, b}))
                            pesos[aresta] = peso
                
                # if *edges in this_line
                else:
                    print(f"Esperado: *edges; lido: {this_line}")
                    return
            # if *vertices in this_line
            else:
                print("Arquivo mal-formado: Não começou com *vertices")
                return
            
            vertices = frozenset(vertices)
            arestas = frozenset(arestas)

            return (vertices, arestas, pesos, rotulos)
            
