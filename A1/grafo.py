from abc import ABC

class Grafo(ABC):

    def __init__(self, vertices: set, edges: set[tuple]) -> None:
        self.__vertices = vertices
        self.__edges = edges
        self.__vertices_enum = list(enumerate(self.__vertices))

    @property
    def vertices(self) -> set:
        return self.__vertices
    
    @property
    def edges(self) -> set:
        return self.__edges
    
    @property
    def vertices_enum(self) -> enumerate:
        return self.__vertices_enum

class GrafoSimples(Grafo):

    def __init__(self, vertices: set, edges: set[tuple]) -> None:
        super().__init__(vertices, edges)
        self.__matrix = self.__generate_adjacency_matrix()
        self.__adj_list = self.__generate_adjacency_list()

    @property
    def matrix(self) -> list:
        '''
        Adjacency matrix for this graph.
        '''
        return self.__matrix
        
    @property
    def adj_list(self) -> dict:
        '''
        Adjacency list for this graph.
        '''
        return self.__adj_list

    def __generate_adjacency_matrix(self) -> list[list]:
        matrix = list(range(len(self.vertices)))
        for row, v in self.vertices_enum:
            neighbours = list()
            for _, u in self.vertices_enum:
                if (v, u) in self.edges or (u, v) in self.edges:
                    neighbours.append(1)
                else:
                    neighbours.append(0)
                
                matrix[row] = neighbours

        self.__matrix = matrix
        return matrix
    
    def simplified_adjacency_matrix(self) -> list[list]:
        '''
        Returns a copy of the adjacency matrix reduced to the lower triangular form.\n
        Does not simplify in-place: the attribute within the Graph\n
        object will still be the complete matrix. Only makes sense if\n
        the Graph in question is purely GrafoSimples.
        '''
        reduced_matrix = list()
        for i, row in enumerate(self.matrix):
            reduced_matrix.append(list(row)[0:i+1:1])

        return reduced_matrix
  
    def __generate_adjacency_list(self) -> dict:
        adj_list = dict()
        for v in self.vertices:
            neighbours = list()
            for u in self.vertices.difference({v}):
                if (v, u) in self.edges or (u, v) in self.edges:
                    neighbours.append(u)
            adj_list[v] = neighbours

        self.__adj_list = adj_list
        return adj_list

# TODO
class GrafoPonderado(GrafoSimples): ...

def test_graph() :
    V = {'a', 'b', 'c'}
    E = {('a', 'b'), ('b', 'c')}
    G = GrafoSimples(V, E)
    G.__generate_adjacency_matrix()

    for e in G.vertices_enum:
        print(e)

    for m in G.matrix:
        print(m)

    print("=====")

    for k in G.__simplified_adjacency_matrix():
        print(k)

    print("=====")

    G.__generate_adjacency_list()

    for k in G.vertices:
        print(f"{k}: {G.adj_list[k]}")

test_graph()