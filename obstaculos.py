import numpy as np
from collections import deque
import random

def indiceAleatorio(limite):
    return random.randint(0,limite-1)


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
    tablero = np.arange(start=1, stop=((cantidadFilas*cantidadFilas)+1), step=1).reshape(cantidadFilas,cantidadFilas)
    
    tablero = generarObstaculos(tablero, obstaculos=5)

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