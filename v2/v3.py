from anytree import Node, PreOrderIter, RenderTree
from anytree.exporter import UniqueDotExporter
import numpy as np
import pygraphviz as pvg
import random
import os, hashlib
from tkinter import *
from tkinter import messagebox
import cv2
# import pygame

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

def buscarAlosAlrededores(pila, nodoPadre, tablero, x, y, profundidadMaxima, raiz):
	print(raiz.height)
	if(nodoPadre.depth <= profundidadMaxima and nodoPadre.name != -100):
		# Ir hacia arriba
		try:
			if tablero[x-1][y] != -1 and x > 0:
				# print(f'El nodo [{nodoPadre.name}] va hacia arriba')
				debeAgregarHijo = validarSiElValorLoTieneMiPapa(nodoPadre, tablero[x-1][y])
				if debeAgregarHijo == False:
					id_ = uniqueID()
					nuevoNodoHijo = Node(tablero[x-1][y], parent=nodoPadre, id=id_)
					pila.append(nuevoNodoHijo)
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x-1, y, profundidadMaxima, raiz)

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
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x, y+1, profundidadMaxima, raiz)

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
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x+1, y, profundidadMaxima, raiz)

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
					buscarAlosAlrededores(pila, nuevoNodoHijo, tablero, x, y-1, profundidadMaxima, raiz)

		except IndexError:
			print("No se puede ir hacia la izquierda")

def arriba(nodoPadre, tablero, x, y):
	print(f'Nodo [ {nodoPadre.name} ] hacia arriba')
	# Ir hacia arriba
	try:
		if tablero[x][y] != -1 and x > 0:
			id_ = uniqueID()
			# nuevoNodoHijo = Node(tablero[x][y], parent=nodoPadre, id=id_)
			nuevoNodoHijo = Node(tablero[x][y], parent=nodoPadre, id=id_)
			nodoPadre.children = [nuevoNodoHijo]
			return nodoPadre
	except IndexError:
		print("No puede ir hacia arriba")
	return nodoPadre

def derecha(nodoPadre, tablero, x, y):
	print(f'Nodo [ {nodoPadre.name} ] hacia derecha')
	# Ir hacia la derecha
	try:
		if tablero[x][y] != -1:
			id_ = uniqueID()
			nuevoNodoHijo = Node(tablero[x][y], parent=nodoPadre, id=id_)
			nodoPadre.children = [nuevoNodoHijo]
	except IndexError:
		print("No se puede ir hacia la derecha")
	return nodoPadre

def abajo(nodoPadre, tablero, x, y):
	print(f'Nodo [ {nodoPadre.name} ] hacia abajo')
	# Ir hacia abajo
	try:
		if tablero[x][y] != -1:
			id_ = uniqueID()
			nuevoNodoHijo = Node(tablero[x][y], parent=nodoPadre, id=id_)
			nodoPadre.children = [nuevoNodoHijo]
	except IndexError:
		print("No se puede ir hacia abajo")
	return nodoPadre

def izquierda(nodoPadre, tablero, x, y):
	print(f'Nodo [ {nodoPadre.name} ] hacia izquierda')
	# Ir hacia la izquierda
	try:
		if tablero[x][y] != -1:
			id_ = uniqueID()
			nuevoNodoHijo = Node(tablero[x][y], parent=nodoPadre, id=id_)
			nodoPadre.children = [nuevoNodoHijo]
	except IndexError:
		print("No se puede ir hacia la izquierda")
	return nodoPadre

def showRecorridos(nodoPadre, tablero):
	soluciones = []

	DFS = PreOrderIter(nodoPadre)
	print("\nDFS:\n")
	
	for nodo in DFS:
		if nodo.name == -100:
			soluciones.append(nodo)
	print("\n\n=== SOLUCIONES === \n\n")
	print(soluciones)
	

def getCoords(tablero, valorBuscado):
	tmp = np.array(tablero)
	return np.where(tmp==valorBuscado, )


def doAlgorithm(size, obstaculos):
	tablero, xInicio, yInicio = construirTablero(size, obstaculos)
	expansionMaxima = 0
	for row in tablero:
			for col in row:
				if col != -1:
					expansionMaxima += 1
	expansionMaxima *= 2
	print(f'Numero de estados => {expansionMaxima}')
	if tablero[xInicio][yInicio] != 0:
		messagebox.showerror(message="Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...", title="Upss")
		raise Exception("Por azares del destino, el tablero no cuenta con una casilla de salida, que mala suerte...")

	nodoRaiz = Node(tablero[xInicio][yInicio], id=uniqueID())
	nodoCursor = None
	pilaDeNodos = []

	mostrarTablero(tablero)
	
	# buscarAlosAlrededores(pilaDeNodos, nodoRaiz, tablero, xInicio, yInicio, expansionMaxima, nodoRaiz)
	recorridoProfundidad = PreOrderIter(nodoRaiz)
	# print(RenderTree(recorridoProfundidad))
	iteracion = 1
	for ultimoNodoDFS in recorridoProfundidad:
		print(nodoRaiz)
		if nodoRaiz.height > expansionMaxima:
			break
		if nodoRaiz.depth > expansionMaxima:
			break
		print(f"Iteracion {iteracion}")
		nodoCursor = ultimoNodoDFS

		coords = getCoords(tablero, nodoCursor.name)
		x_ = int(coords[0])
		y_ = int(coords[1])


		# Ir hacia arriba
		try:
			if tablero[x_-1][y_] != -1 and x_ > 0:
				id_ = uniqueID()
				nodoCursor = Node(tablero[x_-1][y_], parent=nodoCursor, id=id_)
		except IndexError:
			print("No puede ir hacia arriba")

		# Ir hacia la derecha
		try:
			if tablero[x_][y_+1] != -1:
				id_ = uniqueID()
				nodoCursor = Node(tablero[x_][y_+1], parent=nodoCursor, id=id_)
		except IndexError:
			print("No se puede ir hacia la derecha")

		# Ir hacia abajo
		try:
			if tablero[x_+1][y_] != -1 and x_ > 0:
				id_ = uniqueID()
				nodoCursor = Node(tablero[x_+1][y_], parent=nodoCursor, id=id_)
		except IndexError:
			print("No puede ir hacia abajo")

		# Ir hacia la izquierda
		try:
			if tablero[x_][y_-1] != -1:
				id_ = uniqueID()
				nodoCursor = Node(tablero[x_][y_-1], parent=nodoCursor, id=id_)
		except IndexError:
			print("No se puede ir hacia la derecha")
		iteracion +=1


	UniqueDotExporter(nodoRaiz).to_picture("arbol_unique.png")

	# showRecorridos(nodoRaiz, tablero)
	imagenResultante = cv2.imread("arbol_unique.png", cv2.IMREAD_GRAYSCALE)
	cv2.imshow('Arbol resultante', imagenResultante)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
			
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
	txtCuadSize.config(state=NORMAL)

	lblObstAmmount = Label(window, text="Número de obstáculos: ", font=("Arial Bold", 15))
	lblObstAmmount.grid(column=0, row=1)
	txtObstAmmount = Entry(window, width=10)
	txtObstAmmount.grid(column=1, row=1)
	txtObstAmmount.config(state=NORMAL)
	

	btnStart = Button(window, text="Let's go!", fg="black", command=lambda: evaluarEntradas(int(txtCuadSize.get()), int(txtObstAmmount.get()), txtCuadSize, txtObstAmmount))
	btnStart.grid(column=0, row=2)
	window.mainloop()