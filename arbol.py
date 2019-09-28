# Lógica del arbol
# Creado por Luis Fernando Hernandez Morales
# Diseño de sistemas inteligentes - IDS 9A - Universidad Politécnica de Chiapas

from anytree.dotexport import RenderTreeGraph
from anytree import Node
import pygraphviz as pvg
import numpy as np
import string

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

if __name__ == "__main__":
    contadorErrores = 0
    letras = np.array(list(string.ascii_uppercase))
    np.random.shuffle(letras.flat)
    nodos = []
    raiz = Node("NULL")
    for letra in letras:
        nodo = Node(letra,parent=raiz)
        nodos.append(nodo)
    
    # while(contadorErrores <= 4):
    for nodo in nodos:
        letraDelNodo = nodo.name
        letrasDisponibles = diff(letras, np.array([letraDelNodo]))[:5]
        nuevosNodos = []
        print(letrasDisponibles)
        for ld in letrasDisponibles:
            nuevosNodos.append(Node(ld))
        nodo.children = nuevosNodos
    # contadorErrores += 1
    
    RenderTreeGraph(raiz).to_picture("arbol.png")



    # g = pvg.AGraph(strict=False, directed=True)
    # for letra in letras:
    #     g.add_node(letra)
    # g.layout()
    # g.draw('arbol.png')

    
    