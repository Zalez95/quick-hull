# Daniel Gonzalez Alonso
# Script para mostrar el algoritmo QuickHull en blender

import bpy
import threading
import quickHull

def creaLados(vertices):
	""" Dada una lista de vertices, devuelve una lista con los lados
	creados por los vertices en el orden en que llegaron,
	uniendo el ultimo con el primer vertice.
	"""
	lados = []
	for i in range(len(vertices)-1):
		lados.append((i, i+1))
	lados.append((i+1,0))
	return lados

def muestraPunto(v, posicionInicial):
	""" Crea un objeto Empty y lo coloca en la posicion del vertice
	v + posicionInicial.
	"""
	tmp = v + posicionInicial
	bpy.ops.object.add(type='EMPTY', location=tmp)

def muestraLado(v1, v2, posicionInicial):
	""" Muestra un segmento desde v1 hasta v2 en posicionInicial.
	"""
	vertices = [v1, v2]
	lados = [(0, 1)]
	caras = []
	meshLado = bpy.data.meshes.new("lado")
	objLado = bpy.data.objects.new("lado", meshLado)

	# coloco el objeto lado en la misma posicion que el cursor
	objLado.location = posicionInicial

	# enlazo el objeto lado a la escena
	bpy.context.scene.objects.link(objLado)

	# creo la maya del objeto lado
	meshLado.from_pydata(vertices,lados,caras)
	meshLado.update(calc_edges=True)

	return objLado

def borraObjeto(objeto):
	""" Desenlazo el objeto dado y lo borro de la escena.
	"""
	for sce in bpy.data.scenes:
	    try:    sce.objects.unlink(objeto)
	    except:    pass

	bpy.data.objects.remove(objeto)

def algoritmo(posicionInicial):
	""" Crea un objeto de la clase quickHull para mostrar el algoritmo
	por pantalla, en posicionInicial esta la posicion donde se mostrara.
	"""
	global vertices, lados

	# Inicio el algoritmo QuickHull y almacenare el resultado en vertices
	convex = quickHull.QuickHull(posicionInicial)
	vertices = convex.quickHull(verticesObjeto)
	print("\nVertices en la envolvente convexa:\n")
	for vertex in (vertices):
		print(vertex)

	# creo la lista de lados a partir del los vertices de la envolvente
	lados = creaLados(vertices)

	# creo la maya y el objeto
	mi_mesh = bpy.data.meshes.new(nombre)
	mi_objeto = bpy.data.objects.new(nombre, mi_mesh)

	# coloco el objeto en la misma posicion en la que estaba el objeto
	# anteriormente seleccionado.
	mi_objeto.location = posicionInicial

	# enlazo el objeto a la escena
	bpy.context.scene.objects.link(mi_objeto)

	# creo el la maya del objeto
	mi_mesh.from_pydata(vertices,lados,caras)
	mi_mesh.update(calc_edges=True)

if __name__ == "__main__":
	# nombre del objeto y de su maya
	nombre = "ConvexHull"
	# vertices ha de ser una lista de tuplas con las coordenadas x,y,z
	# de cada vertice.
	vertices = []
	# lados ha de ser una lista de tuplas con dos indices a cada vertice
	# de la lista de vertices, los cuales formaran el segmento.
	lados = []
	# caras ha de ser una lista de tuplas con los indices a cada vertice
	# de la lista de vertices, los cuales forman el poligono de cada cara.
	caras= []

	# guardo en verticesObjeto los vertices del objeto seleccionado
	objetoSeleccionado = bpy.context.active_object
	print(objetoSeleccionado)
	if(objetoSeleccionado != None):
		verticesObjeto = []
		print("\nObjeto seleccionado: ", objetoSeleccionado.name)
		if objetoSeleccionado.type == 'MESH':
			for vertex in objetoSeleccionado.data.vertices:
				verticesObjeto.append(vertex.co)
				print(vertex.co)

		# Creo un hilo para ejecutar el algoritmo y le paso la tupla con
		# la posicion del objeto seleccionado
		hilo = threading.Thread(target=algoritmo,
									args=[objetoSeleccionado.location])
		hilo.start()
	else:
		print("No has seleccionado ningun objeto.")