from grafos import ler

feliz_brazil = "../instancias/dirigidos/Feliz, Brazil.net" # Estoura o limite de recursão do python
dirigido1 = "../instancias/dirigidos/dirigido1.net"
dirigido2 = "../instancias/dirigidos/dirigido2.net"
agm = "../instancias/arvore_geradora_minima/agm_tiny.net"

GD = ler(dirigido1, dirigido = True)

print("## Componentes Conexas ##")
GD.componentes_conexas()
print()

print("## Ordenação Topológica ##")
GD.ordenacao_topologica()
print()

print("## Árvore Mínima Geradora ##")
GD.arvore_minima_geradora()
