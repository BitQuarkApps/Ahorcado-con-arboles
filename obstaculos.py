from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter
from anytree import Node, PreOrderIter, RenderTree
import pygraphviz as pvg
import numpy as np
from collections import deque
import random
import os, hashlib, sys
import pprint

def uniqueID():
    return hashlib.md5(os.urandom(32)).hexdigest()[:3]

def indiceAleatorio(limite):
    return random.randint(0,limite-1)


def encontrarNodosEnLasCuatroDirecciones(tablero, xInicio, yInicio, nodoPadre):
    print("Explorando el tablero...\n")
    hijosCreados = []
    str_ = f'{nodoPadre.name}'
    print(f'{nodoPadre.name}')
    if(str_ == "[-100]"):
        return nodoPadre
    # Arriba
    try: 
        if(tablero[xInicio-1, yInicio] != -1):
            unique_id = uniqueID()
            hijosCreados.append(Node(tablero[xInicio-1, yInicio], id=unique_id, parent=nodoPadre))
    except IndexError:
        print('no puede ir hacia arriba')
    # Derecha
    try:
        if(tablero[xInicio, yInicio+1] != -1):
            unique_id = uniqueID()  
            hijosCreados.append(Node(tablero[xInicio, yInicio+1], id=unique_id, parent=nodoPadre))
    except IndexError:
        print('no puede ir hacia la derecha')
    
    # Izquierda
    try:
        if(tablero[xInicio, yInicio-1] != -1):
            unique_id = uniqueID()
            hijosCreados.append(Node(tablero[xInicio, yInicio-1], id=unique_id, parent=nodoPadre))
    except IndexError:
        print('no puede ir hacia la izquierda')
    
    # Abajo
    try:
        if(tablero[xInicio+1, yInicio] != -1):
            unique_id = uniqueID()
            hijosCreados.append(Node(tablero[xInicio+1, yInicio], id=unique_id, parent=nodoPadre))
    except IndexError:
        print('no puede ir hacia abajo')

    nodoPadre.children = hijosCreados
    return nodoPadre

def generarObstaculos(tablero, obstaculos=3):
    """
    Generar obstáculos de manera aleatoria en el tablero.

    Parámetros:
    tablero (array): Tablero del juego.

    obstáculos (int): Cantidad de obstáculos. no puede ser mayor o igual la cantidad de casillas del tablero.

    Regresa:

    Tablero con obstáculos aleatorios
    """
    for i in range(obstaculos+1):
        x = indiceAleatorio(len(tablero))
        y = indiceAleatorio(len(tablero[0]))
        tablero[x][y] = -1  # Obstáculo
    return tablero
    
arbol = []  # Árbol con los nodos generados

# ---------- Búsqueda recursiva por el tablero y generación del árbol de búsqueda ----------

def recorridoTablero(tablero, x, y):
    print("Haciendo recorrido....")
    try:
        if(tablero[x][y] != -100 or tablero[x][y] != -1):
            recorridoTablero(tablero, recorrerArriba(tablero, x, y), y)
            recorridoTablero(tablero, x, recorrerDerecha(tablero, x, y))
            recorridoTablero(tablero, recorrerAbajo(tablero, x, y), y)
            recorridoTablero(tablero, x, recorrerIzquierda(tablero, x, y))
    except IndexError:
        print('Fuera de limites')

# ---------- Métodos para recorrer el tablero ----------
def recorrerArriba(tablero, x, y):
    try:
        x-=1
        if(tablero[x][y] != -100 or tablero[x][y] != -1):
            unique_id = uniqueID()
            parentNode = Node(tablero[x+1][y], id=unique_id)
            unique_id = uniqueID()
            arbol.append(Node(tablero[x][y], id=unique_id, parent=parentNode))
            print(f'ARRIBA => {tablero[x][y]}')
    except IndexError:
        print('Fuera de limites [ARRIBA]')

    return x

def recorrerDerecha(tablero, x, y):
    try:
        y+=1
        if(tablero[x][y] != -100 or tablero[x][y] != -1):
            unique_id = uniqueID()
            parentNode = Node(tablero[x][y-1], id=unique_id)
            unique_id = uniqueID()
            arbol.append(Node(tablero[x][y], id=unique_id, parent=parentNode))
            print(f'DERECHA => {tablero[x][y]}')
    except IndexError:
        print('Fuera de limites [DERECHA]')

    return y

def recorrerAbajo(tablero, x, y):
    try:
        x+=1
        if(tablero[x][y] != -100 or tablero[x][y] != -1):
            unique_id = uniqueID()
            parentNode = Node(tablero[x-1][y], id=unique_id)
            unique_id = uniqueID()
            arbol.append(Node(tablero[x][y], id=unique_id, parent=parentNode))
            print(f'ABAJO => {tablero[x][y]}')
    except IndexError:
        print('Fuera de limites [ABAJO]')

    return x
    
def recorrerIzquierda(tablero, x, y):
    try:
        y-=1
        if(tablero[x][y] != -100 or tablero[x][y] != -1):
            unique_id = uniqueID()
            parentNode = Node(tablero[x][y+1], id=unique_id)
            unique_id = uniqueID()
            arbol.append(Node(tablero[x][y], id=unique_id, parent=parentNode))
            print(f'IZQUIERDA => {tablero[x][y]}')
    except IndexError:
        print('Fuera de limites [IZQUIERDA]')

    return y

if __name__ == "__main__":
    cantidadFilas = 3
    obstaculos_ = 1
    
    tablero = []
    contador = 0
    for i in range(0, cantidadFilas):
        row = []
        for j in range(contador+1, (contador + cantidadFilas)+1):
            row.append(j)
            contador = j
        tablero.append(row)

    tablero = generarObstaculos(tablero, obstaculos=obstaculos_)
    
    xInicio = indiceAleatorio(len(tablero))
    yInicio = indiceAleatorio(len(tablero[0]))

    xSalida = indiceAleatorio(len(tablero))
    ySalida = indiceAleatorio(len(tablero[0]))
    tablero[xInicio][yInicio] = 0
    # Fijar la casilla final
    tablero[xSalida][ySalida] = -100

    pprint.pprint(tablero, indent=4)
    # raiz_id = uniqueID()
    # nodoRaiz = Node(tablero[xInicio][yInicio], id=raiz_id)# Raíz del árbol
    sys.setrecursionlimit(10000)
    recorridoTablero(tablero, xInicio, yInicio)

    # nodoRaiz = encontrarNodosEnLasCuatroDirecciones(tablero, xInicio, yInicio, nodoRaiz)
    # print(RenderTree(nodoRaiz))

    # print("Realizando busqueda en profundidad para la raíz")
    # cola = []
    
    # for hijo in nodoRaiz.children:
    #     cola.append(hijo)
    #     posicionDelNodoEnLaMatriz = np.where(tablero == hijo.name)
    #     posicionX = posicionDelNodoEnLaMatriz[0]
    #     posicionY = posicionDelNodoEnLaMatriz[1]
    #     hijo = encontrarNodosEnLasCuatroDirecciones(tablero, posicionX, posicionY, hijo)
    

    # # Aquí se cicla :"v
    # while len(cola) > 0:
    #     nodoCursor = cola.pop(0)
    #     for hijo in nodoCursor.children:
    #         cola.append(hijo)
    #         posicionDelNodoEnLaMatriz = np.where(tablero == hijo.name)
    #         posicionX = posicionDelNodoEnLaMatriz[0]
    #         posicionY = posicionDelNodoEnLaMatriz[1]
    #         hijo = encontrarNodosEnLasCuatroDirecciones(tablero, posicionX, posicionY, hijo)

    raizArbol = arbol.pop(0) # Obtener el primero

    # print('Exportando a .dot ...')
    DotExporter(raizArbol).to_dotfile('arbol.dot')
    # print('Exportando a una imagen ...')
    #Generar imagen con el formato .dot
    G=pvg.AGraph("arbol.dot")
    G.layout(prog='dot')
    G.draw('arbol_dot.png')