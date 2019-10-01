from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter
from anytree import Node, PreOrderIter, RenderTree
import pygraphviz as pvg
import numpy as np
from collections import deque
import random
import os, hashlib

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
        x = indiceAleatorio(tablero.shape[0])
        y = indiceAleatorio(tablero.shape[1])
        tablero[x][y] = -1  # Obstáculo
    return tablero
    

if __name__ == "__main__":
    cantidadFilas = 5
    obstaculos_ = 3
    tablero = np.arange(start=1, stop=((cantidadFilas*cantidadFilas)+1), step=1).reshape(cantidadFilas,cantidadFilas)

    tablero = generarObstaculos(tablero, obstaculos=obstaculos_)

    while(0 not in tablero):
        xInicio = indiceAleatorio(tablero.shape[0])
        yInicio = indiceAleatorio(tablero.shape[1])

        xSalida = indiceAleatorio(tablero.shape[0])
        ySalida = indiceAleatorio(tablero.shape[1])

        if(tablero[xInicio][yInicio] != -1):
            if(tablero[xSalida][ySalida] != -1):
                # Fijar la casilla de salida con [0]
                tablero[xInicio][yInicio] = 0
                # Fijar la casilla final
                tablero[xSalida][ySalida] = -100

    print(tablero)    
    raiz_id = uniqueID()
    nodoRaiz = Node(tablero[xInicio][yInicio], id=raiz_id)# Raíz del árbol

    nodoRaiz = encontrarNodosEnLasCuatroDirecciones(tablero, xInicio, yInicio, nodoRaiz)
    # print(RenderTree(nodoRaiz))

    # print("Realizando busqueda en profundidad para la raíz")
    cola = []
    
    for hijo in nodoRaiz.children:
        cola.append(hijo)
        posicionDelNodoEnLaMatriz = np.where(tablero == hijo.name)
        posicionX = posicionDelNodoEnLaMatriz[0]
        posicionY = posicionDelNodoEnLaMatriz[1]
        hijo = encontrarNodosEnLasCuatroDirecciones(tablero, posicionX, posicionY, hijo)
    
    while len(cola) > 0:
        nodoCursor = cola.pop(0)
        for hijo in nodoCursor.children:
            cola.append(hijo)
            posicionDelNodoEnLaMatriz = np.where(tablero == hijo.name)
            posicionX = posicionDelNodoEnLaMatriz[0]
            posicionY = posicionDelNodoEnLaMatriz[1]
            hijo = encontrarNodosEnLasCuatroDirecciones(tablero, posicionX, posicionY, hijo)



    

    # print('Exportando a .dot ...')
    DotExporter(nodoRaiz).to_dotfile('obstaculos.dot')
    # print('Exportando a una imagen ...')
    #Generar imagen con el formato .dot
    G=pvg.AGraph("obstaculos.dot")
    G.layout(prog='dot')
    G.draw('obstaculos_dot.png')

