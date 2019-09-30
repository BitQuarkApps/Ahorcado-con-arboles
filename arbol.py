# Lógica del arbol
# Creado por Luis Fernando Hernandez Morales
# Diseño de sistemas inteligentes - IDS 9A - Universidad Politécnica de Chiapas

from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter
from anytree import Node, PreOrderIter, RenderTree
import pygraphviz as pvg
import numpy as np
import string
import os, hashlib


_iteracion = 1

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def randomID():
    return hashlib.md5(os.urandom(32)).hexdigest()[:5]

def exportToImage(root, nombre="arbol.png"):
    """
    Exportar el arbol a una imagen

    Parameters:

    root (Node): Nodo raíz.
(raiz)
    name (string): Nombre de la imagen (default: 'arbol.png')
    """
    RenderTreeGraph(root).to_picture(nombre)

def obtenerLetrasDelAbecedario():
    return np.array(list(string.ascii_uppercase))

def primeraLetraDeLaPalabra(palabra, evitar="-"):
    """
    Obtener la primera letra de la palabra.

    Se evitará el caracter '-'

    Parameters:

    palabra (string): Plabra del juego.

    evitar (string): Caracter a evitar (default '-')

    Returns:

    Primer caracter que se encontró
    """
    result = None
    for caracter in palabra:
        if caracter.upper() != evitar:
            result = caracter.upper()
            break
    return result

def reemplazarEnLaPalabra(palabra, reemplazar, reemplazo="-"):
    """
    Reemplazar un caracter por otro en la palabra del juego.

    Parameters:

    palabra (string): Plabra del juego.

    reemplazar (string): Caracter a reemplazar
    
    reemplazo (string): Se cambiará el caracter a reemplazar por este valor (default '-')

    Returns:

    palabra con los caracteres reemplazados
    """
    return palabra.replace(reemplazar, reemplazo)

def encontrarUnNodoConEsteValor(raiz, valor):
    """
    Obtener un nodo con el algoritmo de DFS que contenga el valor solicitado

    Parameters:

    raiz (Node): Raíz del árbol.

    valor (string): Caracter a buscar

    Returns:

    Nodo donde se encuentra
    """
    result = None
    for node in PreOrderIter(raiz):
        if(node.name == valor):
            result = node
            break
    
    return result

def llenarElNodoDeHijosConLasLetrasRestantes(padre, letras):
    """
    Agregar un hijo por letra restante del arreglo de letras.
    Se analizarán a los padres para no repetir las letras

    Parameters:

    padre (Node): Nodo padre.

    letras (array): Arreglo de letras disponibles

    Returns:

    Nodo con sus hijos
    """
    padreCopy = padre
    letrasQueYaSeEncuentran = [] # En cada padre del nodo padre
    letrasQueYaSeEncuentran.append(padreCopy.name)

    letrasRestantes = []
    nuevosNodos = []
    while padreCopy != None:
        padreCopy = padreCopy.parent
        if(padreCopy != None):
            if(padreCopy.name != "NULL"):
                if "_" in padreCopy.name:
                    _split = padreCopy.name.split('_')
                    letrasQueYaSeEncuentran.append(_split[0])
                else:
                    letrasQueYaSeEncuentran.append(padreCopy.name)

    letrasRestantes = diff(letras, letrasQueYaSeEncuentran)
    for restante in letrasRestantes:
        if(restante not in letrasQueYaSeEncuentran):
            id_ = randomID()
            _split = padreCopy.name.split('_')
            nuevosNodos.append(Node(f'{restante}_{id_}', id=id_, parent=padre))
    
    padre.children = nuevosNodos
    return padre
    # padre_ = 1
    # while (padre_ != "/NULL"):
    #     padre_ = padre.name
    #     letrasQueYaSeEncuentran.append(padre_)
    #     padre_ = padre.parent
    #     print(padre_)
        
    


def construirArbolConLaPalabra(palabra, letras, niveles=1):
    """Construye el árbol con las letras correctas e incorrectas.
    
    Parameters:

    palabra (string): La palabra que se tiene que adivinar.

    letras (array): Arreglo de letras que tiene el abecedario, es necesario que sea completo, las diferencias se calcularán aquí.
    niveles (int): Profundidad máxima (default 5)

    Returns:

    Raíz del árbol construido con todos sus hijos
    """
    raiz = Node("NULL")
    for letra in letras:
        id_ = randomID()
        nodo = Node(letra, id=id_, parent=raiz)
    
    # while (niveles >= 1):
        # for nodo in raiz.children:
        #     nodo = llenarElNodoDeHijosConLasLetrasRestantes(nodo, letras)
    for nodo in PreOrderIter(raiz):
        nodo = llenarElNodoDeHijosConLasLetrasRestantes(nodo, letras)
        # niveles -= 1
    return raiz


if __name__ == "__main__":
    letras = obtenerLetrasDelAbecedario()[:3]
    # np.random.shuffle(letras.flat) # Ordenar de manera aleatoria
    print('Construyendo arbol ...')
    raiz = construirArbolConLaPalabra("PEZ", letras)

    # exportToImage(raiz)

    #exportar al archivo .dot para abrir con graphviz
    print('Exportando a .dot ...')
    DotExporter(raiz).to_dotfile('arbol.dot')
    print('Exportando a una imagen ...')
    #Generar imagen con el formato .dot
    G=pvg.AGraph("arbol.dot")
    G.layout(prog='dot')
    G.draw('arbol_dot.png')

    
    