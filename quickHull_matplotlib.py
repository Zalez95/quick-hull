#Daniel Gonzalez Alonso
#Algoritmo QuickHull en python con visualizacion en matplotlib.

try:
	import matplotlib.patches as patches
	import pylab
except ImportError:
    raise ImportError("Se necesita instalar matplotlib")
import random


# Numero maximo de vertices a analizar.
NUMERO_VERTICES = 30
# Maxima posicion en el eje X e Y donde se situaran los vertices.
MAX = 10

# Indices a la posicion del valor en cada eje del vertice.
EJE_X = 0
EJE_Y = 1
EJE_Z = 2

class QuickHull:
	""" Algoritmo QuickHull para calcular la envolvente convexa 2D de 
	una serie de vertices mediante un algoritmo divide y venceras.
	"""

	def __init__(self):
		""" Constructor de la clase.

		Atributos:
			envolvente: lista en la cual se almacenara la envolvente
				calculada.
			posicionInicial: posicion donde se visualizaran los
			puntos en Blender.
		"""
		self.envolvente = []

	def quickHull(self, listaVertices):
		""" Inicio del algoritmo QuickHull: divide el conjunto de puntos 
		en dos subconjuntos dependiendo de si estan por encima o por 
		debajo de la recta formada por el minimo y el maximo punto en 
		el eje X y los introduce en la envolvente, despues busca mas
		puntos de la envolvente en los subconjuntos formados mediante
		subHull. Finalmente retorna la envolvente.

		Solo se ejeuta el algoritmo, si listaVertices tiene mas de tres
		vertices, si tiene tres o menos, ya se sabe que esos puntos
		estan dentro de la envolvente.

		Parametros:
			listaVertices: lista con los vertices de los cuales queremos
				hayar la envolvente.
		"""
		if(len(listaVertices) > 3):
			puntoA = listaVertices.pop(self.minimo(listaVertices, EJE_X))
			puntoB = listaVertices.pop(self.maximo(listaVertices, EJE_X))

			subListaA = self.dividePuntos(puntoA, puntoB, listaVertices)
			subListaB = self.dividePuntos(puntoB, puntoA, listaVertices)

			self.envolvente.append(puntoA)
			self.subHull(puntoA, puntoB, subListaA)
			self.envolvente.append(puntoB)
			self.subHull(puntoB, puntoA, subListaB)
		else:
			self.envolvente = listaVertices
		return self.envolvente

	def subHull(self, puntoA, puntoB, listaVertices):
		""" Calcula el punto de listaVertices mas lejano a la recta 
		formada por A y B, y divide el conjunto de vertices dependiendo 
		de si los puntos estan por encima de la recta formada por A y C
		o por encima de la recta formada por B y C, introduce C
		en la envolvente y busca mas puntos de la envolvente en los 
		subconjuntos formados.

		Parametros:
			puntoA y puntoB: puntos mediante los cuales calcularemos el
				siguiente punto de la envolvente y los siguientes
				subconjuntos.
			listaVertices: lista con los vertices de los cuales queremos
				hayar la envolvente.
		"""
		if(len(listaVertices) != 0):
			puntoC = listaVertices.pop(
				self.puntoMasLejano(puntoA, puntoB, listaVertices))

			subListaA = self.dividePuntos(puntoA, puntoC, listaVertices)
			subListaB = self.dividePuntos(puntoC, puntoB, listaVertices)

			self.subHull(puntoA, puntoC, subListaA)
			self.envolvente.append(puntoC)
			self.subHull(puntoC, puntoB, subListaB)

	def maximo(self, listaVertices, eje):
		""" Retorna el indice del vertice de listaVertices con el maximo
		valor en el eje seleccionado.

		Parametros:
			listaVertices: lista con los vertices de los cuales queremos
				hayar el maximo.
			eje: eje de los vertices en el cual queremos hayar el maximo.
		"""
		maximoactual = 0
		for i in range(1, len(listaVertices)):
			if (listaVertices[i][eje] > listaVertices[maximoactual][eje]):
				maximoactual = i
		return maximoactual

	def minimo(self, listaVertices, eje):
		""" Retorna el indice del vertice de listaVertices con el minimo
		valor en el eje seleccionado.

		Parametros:
			listaVertices: lista con los vertices de los cuales queremos
				hayar el minimo.
			eje: eje de los vertices en el cual queremos hayar el minimo.
		"""
		minimoactual = 0
		for i in range(1, len(listaVertices)):
			if (listaVertices[i][eje] < listaVertices[minimoactual][eje]):
				minimoactual = i
		return minimoactual

	def distanciaPuntoRecta(self, puntoRA, puntoRB, puntoC):
		""" Retorna la distancia de puntoC a la recta formada por puntoRA
		y puntoRB (sin dividir por el modulo).
		
		Formula para calcular la distancia de un punto a una recta:
			d = ((Bx-Ax)(Cy-Ay) - (By-Ay)(Cx-Ax)) / sqrt((Bx-Ax)^2 + (By-Ay)^2)

		Parametros:
			puntoRA: primer punto de la recta.
			puntoRB: segundo punto de la recta.
			puntoC: punto del cual calcularemos la distancia.
		"""
		difY = puntoRB[EJE_Y] - puntoRA[EJE_Y]
		difX = puntoRB[EJE_X] - puntoRA[EJE_X]
		return abs(difX*(puntoC[EJE_Y] - puntoRA[EJE_Y]) - \
			difY*(puntoC[EJE_X] - puntoRA[EJE_X]))

	def puntoMasLejano(self, puntoRA, puntoRB, listaVertices):
		""" Retorna un indice al punto de listaVertices que se encuentra 
		mas lejos a la recta formada por puntoRA y puntoRB.

		Parametros:
			puntoRA: primer punto de la recta.
			puntoRB: segundo punto de la recta.
			listaVertices: lista con los vertices de los cuales queremos
				hayar punto mas lejano.
		"""
		indice = 0
		distMaxima = self.distanciaPuntoRecta(
			puntoRA, puntoRB, listaVertices[indice])
		for i in range(1, len(listaVertices)):
			distI = self.distanciaPuntoRecta(
				puntoRA, puntoRB, listaVertices[i])
			if(distMaxima < distI):
				indice = i
				distMaxima = distI
		return indice

	def estaPuntoDerecha(self, puntoRA, puntoRB, puntoC):
		""" Retorna Verdadero si puntoC esta por encima de la recta
		formada por puntoRA y puntoRB.

		Parametros:
			puntoRA: primer punto de la recta.
			puntoRB: segundo punto de la recta.
			puntoC: punto del cual queremos saber si esta por encima o
				por debajo de la recta.
		"""
		difY = puntoRB[EJE_Y] - puntoRA[EJE_Y]
		difX = puntoRB[EJE_X] - puntoRA[EJE_X]
		resultado = difX*(puntoC[EJE_Y] - puntoRA[EJE_Y]) - \
			difY*(puntoC[EJE_X] - puntoRA[EJE_X])
		if(resultado > 0):
			return True
		return False

	def dividePuntos(self, puntoRA, puntoRB, listaVertices):
		""" Retorna una lista con los puntos que estan por encima de la 
		recta formada por puntoRA y puntoRB.

		Parametros:
			puntoRA: primer punto de la recta.
			puntoRB: segundo punto de la recta.
			listaVertices: lista con los vertices de los cuales queremos
				comprobar cuales estan por encima.
		"""
		listaPuntosD = []
		for i in (listaVertices):
			if(self.estaPuntoDerecha(puntoRA, puntoRB, i)):
				listaPuntosD.append(i)
		return listaPuntosD

def main():
	""" Creo un objeto de QuickHull y calculo la envolvente de unos
	vertices creados aleatoriamente, despues muestro el resultado por
	pantalla.
	"""
	vertices = []
	for i in range(NUMERO_VERTICES):
		vertices.append((random.randint(-MAX,MAX), random.randint(-MAX,MAX)))

	convexHull = QuickHull()
	res = convexHull.quickHull(vertices)
	print(res)

	pylab.scatter([p[0] for p in vertices], [p[1] for p in vertices])
	pylab.scatter([p[0] for p in res], [p[1] for p in res], color = 'R')
	pylab.gca().add_patch(patches.Polygon(res, closed=True, fill=False))
	pylab.grid()
	pylab.show()

if __name__ == "__main__":
	main()