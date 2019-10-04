from anytree import Node, PreOrderIter, RenderTree
from anytree.exporter import UniqueDotExporter
from prettytable import PrettyTable
import pygraphviz as pvg
import numpy as np
import random
import pprint
import os, hashlib
from tkinter import *
from tkinter import messagebox
import cv2
import pygame

def uniqueID():
    return hashlib.md5(os.urandom(32)).hexdigest()[:5]

def indiceAleatorio(limite):
	return random.randint(0,limite-1)

def construirTablero(cantidadFilas, obstaculos_):
	tablero = []
	cantidadFilas = cantidadFilas
	obstaculos_ = obstaculos_

	tablero = []
	contador = 0
	for i in range(0, cantidadFilas):
		row = []
		for j in range(contador+1, (contador + cantidadFilas)+1):
			row.append(j)
			contador = j
		tablero.append(row)

	for i in range(obstaculos_):
		x = indiceAleatorio(len(tablero))
		y = indiceAleatorio(len(tablero[0]))
		tablero[x][y] = -1  # Obstáculo

	xInicio = indiceAleatorio(len(tablero))
	yInicio = indiceAleatorio(len(tablero[0]))

	xSalida = indiceAleatorio(len(tablero))
	ySalida = indiceAleatorio(len(tablero[0]))
	tablero[xInicio][yInicio] = 0
	# Fijar la casilla final
	tablero[xSalida][ySalida] = -100

	return tablero, xInicio, yInicio

def mostrarTablero(tablero):
	print("\n")
	for row in tablero:
		print(row)
	print("\n")

def validarSiElValorLoTieneMiPapa(nodoHijo, valor):
	copia = nodoHijo.parent
	while copia != None:
		if(copia.name == valor):
			return True
		copia = copia.parent
	return False

def buscarAlosAlrededores(pila, nodoPadre, tablero, x, y):

	if(nodoPadre.name != -100):
		# Ir hacia arriba
		try:
			if tablero[x-1][y] != -1 and x > 0:
				# print(f'El nodo [{nodoPadre.name}] va hacia arriba')
				debeAgregarHijo = validarSiElValorLoTieneMiPapa(nodoPadre, tablero[x-1][y])
				if debeAgregarHijo == False:
					id_ = uniqueID()
					nuevoNodoHijo = Node(tablero[x-1][y], parent=nodoPadre, id=id_)
					pila.append(nuevoNodoHijo)
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x-1, y)

		except IndexError:
			print("No puede ir hacia arriba")

		# Ir hacia la derecha
		try:
			if tablero[x][y+1] != -1:
				# print(f'El nodo [{nodoPadre.name}] va hacia la derecha')
				debeAgregarHijo = validarSiElValorLoTieneMiPapa(nodoPadre, tablero[x][y+1])
				if debeAgregarHijo == False:
					id_ = uniqueID()
					nuevoNodoHijo = Node(tablero[x][y+1], parent=nodoPadre, id=id_)
					pila.append(nuevoNodoHijo)
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x, y+1)

		except IndexError:
			print("No se puede ir hacia la derecha")

		# Ir hacia abajo
		try:
			if tablero[x+1][y] != -1:
				# print(f'El nodo [{nodoPadre.name}] va hacia abajo')
				debeAgregarHijo = validarSiElValorLoTieneMiPapa(nodoPadre, tablero[x+1][y])
				if debeAgregarHijo == False:
					id_ = uniqueID()
					nuevoNodoHijo = Node(tablero[x+1][y], parent=nodoPadre, id=id_)
					pila.append(nuevoNodoHijo)
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x+1, y)

		except IndexError:
			print("No se puede ir hacia abajo")

		# Ir hacia la izquierda
		try:
			if tablero[x][y-1] != -1 and y > 0:
				# print(f'El nodo [{nodoPadre.name}] va hacia la izquierda')
				debeAgregarHijo = validarSiElValorLoTieneMiPapa(nodoPadre, tablero[x][y-1])
				if debeAgregarHijo == False:
					id_ = uniqueID()
					nuevoNodoHijo = Node(tablero[x][y-1], parent=nodoPadre, id=id_)
					pila.append(nuevoNodoHijo)
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x, y-1)

		except IndexError:
			print("No se puede ir hacia la izquierda")

def showRecorridos(nodoPadre, tablero):
	soluciones = []

	DFS = PreOrderIter(nodoPadre)
	print("\nDFS:\n")
	
	for nodo in DFS:
		if nodo.name == -100:
			soluciones.append(nodo)
	print("\n\n=== SOLUCIONES === \n\n")
	print(soluciones)
	# NEGRO = (0, 0, 0)
	# BLANCO = (255, 255, 255)
	# VERDE = ( 0, 255, 0)
	# ROJO = (255, 0, 0)
	# AZUL = (12, 74, 173)
	# # Establecemos el LARGO y ALTO de cada celda de la retícula.
	# LARGO  = 20
	# ALTO = 20
	# # Establecemos el margen entre las celdas.
	# MARGEN = 5

	# pygame.init()
	# # Establecemos el LARGO y ALTO de la pantalla
	# DIMENSION_VENTANA = [255, 255]
	# pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
	# # Establecemos el título de la pantalla.
	# pygame.display.set_caption("Recorrido")
	# # Iteramos hasta que el usuario pulse el botón de salir.
	# hecho = False
	
	# # Lo usamos para establecer cuán rápido de refresca la pantalla.
	# reloj = pygame.time.Clock()
	# while not hecho:
	# 	for evento in pygame.event.get(): 
	# 		if evento.type == pygame.QUIT:
	# 			hecho = True
		
	# 	pantalla.fill(NEGRO)
	# 	for fila in range(len(tablero)):
	# 		for columna in range(len(tablero[0])):
	# 			color = BLANCO
	# 			if tablero[fila][columna] == 0:
	# 				color = ROJO
	# 			elif tablero[fila][columna] == -100:
	# 				color = AZUL
				
	# 			print(color)
	# 			pygame.draw.rect(pantalla,
    #                          color,
    #                          [(MARGEN+LARGO) * columna + MARGEN,
    #                           (MARGEN+ALTO) * fila + MARGEN,
    #                           LARGO,
    #                           ALTO])
	# 	# Limitamos a 60 fotogramas por segundo.
	# 	reloj.tick(60)
	
	# 	# Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
	# 	pygame.display.flip()

		
	
def doAlgorithm(size, obstaculos):
	tablero, xInicio, yInicio = construirTablero(size, obstaculos)
	if tablero[xInicio][yInicio] != 0:
		messagebox.showerror(message="Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...", title="Upss")
		raise Exception("Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...")

	nodoRaiz = Node(tablero[xInicio][yInicio], id=uniqueID())
	pilaDeNodos = []

	mostrarTablero(tablero)
	
	buscarAlosAlrededores(pilaDeNodos, nodoRaiz, tablero, xInicio, yInicio)
	
	UniqueDotExporter(nodoRaiz).to_picture("arbol_unique.png")

	showRecorridos(nodoRaiz, tablero)
	
	imagenResultante = cv2.imread("arbol_unique.png", cv2.IMREAD_COLOR)
	cv2.imshow('Arbol resultante', imagenResultante)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	pygame.quit()
			
def evaluarEntradas(size, obstaculos, txtSize, txtObst):
	txtSize.config(state=DISABLED)
	txtObst.config(state=DISABLED)
	messagebox.showinfo(message="Ejecutando algoritmo", title="Espere por favor....")
	doAlgorithm(size, obstaculos)
	txtSize.config(state=NORMAL)
	txtObst.config(state=NORMAL)
	messagebox.showinfo(message="Algoritmo terminado", title="Información")


if __name__ == "__main__":
	window = Tk()
	window.title("DSI - DFS Obstaculos")
	window.geometry('350x200')	
	# Etiqueta de Tamaño de cuadricula
	lblCuadSize = Label(window, text="Ingresa el tamaño de la cuadrícula: ", font=("Arial Bold", 15))
	lblCuadSize.grid(column=0, row=0)
	txtCuadSize = Entry(window, width=10)
	txtCuadSize.grid(column=1, row=0)

	lblObstAmmount = Label(window, text="Número de obstáculos: ", font=("Arial Bold", 15))
	lblObstAmmount.grid(column=0, row=1)
	txtObstAmmount = Entry(window, width=10)
	txtObstAmmount.grid(column=1, row=1)

	btnStart = Button(window, text="Let's go!", fg="black", command=lambda: evaluarEntradas(int(txtCuadSize.get()), int(txtObstAmmount.get()), txtCuadSize, txtObstAmmount))
	btnStart.grid(column=0, row=2)
	window.mainloop()