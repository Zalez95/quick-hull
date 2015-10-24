# Daniel Gonzalez Alonso
# Script para crear vertices aleatorios en Blender.

import bpy
import random

NUMERO_VERTICES = 30	# Numero de vertices ha mostrar
MAX = 10				# Maxima posicion de los vertices

if __name__ == "__main__":
	"""Script para generar vertices aleatorios en una escena"""
	# nombre del objeto y de su maya
	nombre = "Vertices"
	# vertices a de ser una lista de tuplas con las coordenadas x,y,z de cada vertice
	vertices = []
	# lados ha de ser una lista de tuplas de dos vertices, los cuales forman el
	# segmento de cada lado
	lados = []
	# caras ha de ser una lista de tuplas de varios vertices, los cuales forman el
	# poligono de cada cara
	caras= []

	for i in range(NUMERO_VERTICES):
		vertices.append((random.randint(-MAX,MAX), random.randint(-MAX,MAX), 0))

	# creo la maya y el objeto
	mi_mesh = bpy.data.meshes.new(nombre)
	mi_objeto = bpy.data.objects.new(nombre, mi_mesh)

	# coloco el objeto en la misma posicion que el cursor
	mi_objeto.location = bpy.context.scene.cursor_location

	# link el objeto a la escena
	bpy.context.scene.objects.link(mi_objeto)

	# creo el objeto con una funcion de blender
	mi_mesh.from_pydata(vertices,lados,caras)
	mi_mesh.update(calc_edges=True)
