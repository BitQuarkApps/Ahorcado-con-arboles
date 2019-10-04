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
	copy = np.array(tablero).reshape(len(tablero), len(tablero[0]))
	pprint.pprint(copy)
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

def verPorPrimeraVezMislimites(tablero, x, y):
	resultX = []
	resultY = []
	# Ir hacia arriba
	try:
		if tablero[x-1][y] != -1 and x > 0:
			resultX.append(x-1)
			resultY.append(y)
	except IndexError:
		print("No puede ir hacia arriba")

	# Ir hacia la derecha
	try:
		if tablero[x][y+1] != -1:
			resultX.append(x)
			resultY.append(y+1)
	except IndexError:
		print("No se puede ir hacia la derecha")
	
	# Ir hacia abajo
	try:
		if tablero[x+1][y] != -1:
			resultX.append(x+1)
			resultY.append(y)
	except IndexError:
		print("No se puede ir hacia abajo")

	# Ir hacia la izquierda
		try:
			if tablero[x][y-1] != -1 and y > 0:
				resultX.append(x)
				resultY.append(y-1)
		except IndexError:
			print("No se puede ir hacia la izquierda")
	
	return resultX, resultY


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
			
def evaluarEntradas(size, obstaculos, txtSize, txtObst):
	txtSize.config(state=DISABLED)
	txtObst.config(state=DISABLED)
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