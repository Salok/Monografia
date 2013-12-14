#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import Numpy para trabajar con matrices
import numpy

#Importamos los cuaterniones para rotar objetos
from Quaternion_Class import Quaternion
from Vector3D_Class import Vector3D
import MatrizFunciones as matriz
import WorldParams

wp = WorldParams.WorldParams()
#--------------------------------------------------------------#
#					   Objeto3D class                          #
#--------------------------------------------------------------#

#Los objetos son grupos de vertices y aristas
class Objeto3D:
	#Constructor. Guarda una lista con los vertices, otra con las aristas y otra con las caras. 
	def __init__(self):
		self.vertices = numpy.zeros((0, 4))
		self.aristas = []
		self.caras = []


	#Representación en string de la clase. Para print y debuggear
	def __repr__(self):
		verticesDebug = "\n --- Vertices --- \n"
		for i, (x, y , z, _) in enumerate(self.vertices):
			verticesDebug += "Vertice %d: %d, %d, %d \n" % (i, x, y, z)

		aristasDebug = "\n --- Aristas --- \n"
		for i, (ver1, ver2) in enumerate(self.aristas):
			aristasDebug += "Arista %d: Une los vertices %d y %d \n" % (i, ver1, ver2)

		#Lo juntamos todo y lo devolvemos.
		final = ('Mi centro esta en %r. \n Tengo %r vertices que son: \n' + verticesDebug + 'y %r aristas que son: \n' + aristasDebug) % (self.Centro(), len(self.vertices), len(self.aristas))
		return final

	#Coge una lista de coordenadas y las transforma en vertices para añadir al objeto
	def Vertices(self, listaVertices):
		#Creamos una lista de unos
		unoCol = numpy.ones((len(listaVertices), 1))
		#La añadimos a la lista de coordenadas
		add = numpy.hstack((listaVertices, unoCol))
		#Añadimos la lista de coordenadas a la lista de vertices del objeto
		self.vertices = numpy.vstack((self.vertices, add))

	#Coge una lista de indices de vertices y las convierte en aristas para añadir al objeto
	def Aristas(self, listaAristas):
		self.aristas += listaAristas

	#Coge una lista de caras y su color y las añade a la lista de caras del objeto. La lista de caras es una lista de los vertices de cada cara.
	def Caras(self, listaCaras, color = (255, 255, 255)):
		#Cada lista de vertices es una cara
		for listaVertices in listaCaras:
			numVertices = len(listaVertices)
			#Comprobamos que los identificadores de los vertices no sean mayores que el número de vertices.
			if all((vertice < len(self.vertices) for vertice in listaVertices)):
				#Añadimos las caras con su color
				self.caras.append((listaVertices, numpy.array(color, numpy.uint8)))
				#Añadimos las aristas de la cara
				self.Aristas([(listaVertices[n-1], listaVertices[n]) for n in xrange(numVertices)])



	#Aplicar una matriz de transformación
	def Transformar(self, mat):
		self.vertices = numpy.dot(self.vertices, mat)

	#Rotar el objeto con un cuaternión
	def Rotar(self, qRotacion):
		#Aplicamos el cuaternión a cada uno de los vertices del objeto
		for i, (x, y, z, _) in enumerate(self.vertices):
			rotado = Quaternion(0, x, y, z).Conjugacion(qRotacion)
			self.vertices[i] = [rotado.vector.x, rotado.vector.y, rotado.vector.z, 1]

	#Funcion para calcular el centro de un objeto.
	def Centro(self):
		#Calculamos el valor máximo y el mínimo de todos los vertices
		Min = self.vertices[:,:-1].min(axis=0)
		Max = self.vertices[:,:-1].max(axis=0)

		#Devolvemos el punto medio del intervalo entre el máximo y el mínimo
		return 0.5 * (Min + Max)

	#Alinear el objeto a un punto. Hace que el centro del objeto sea el punto dado.
	def Alinear(self, (px, py, pz)):
		#Creamos un vector con el punto dado
		punto = Vector3D(px, py, pz)
		#Calculamos el centro actual del objeto y creamos un vector con él
		centro = Vector3D(*self.Centro())
		for i, (x, y, z, _) in enumerate(self.vertices):
			#Creamos un vector con cada vertice
			vertice = Vector3D(x, y, z)
			#Calculamos la distancia al centro actual
			dist = vertice - centro
			#Mantenemos la distancia tomando el nuevo punto como centro
			alineado = punto + dist
			self.vertices[i] = [alineado.x, alineado.y, alineado.z, 1]


#--------------------------------------------------------------#
#					   Sistema3D class                         #
#--------------------------------------------------------------#
#Sistema de objetos. Todos los objetos de un sistema se consideran uno único al realizar las transformaciones
class Sistema3D:
	#Constructor
	def __init__(self, ID):
		self.ID = ID
		self.objetos = {}

	#Representación en string de la clase. Para print y debuggear
	def __repr__(self):
		debug = 'Sistema %r. Estoy compuesto por los objetos: \n' % (self.ID)
		for nombre, objeto in self.objetos.iteritems():
			debug += ('Objeto %r: ' % (nombre) + Objeto3D.__repr__(objeto))
			debug += '\n'

		return debug

	#Añadimos un nuevo objeto al sistema
	def nuevoObjeto(self, nombre, objeto):
		self.objetos[nombre] = objeto

	
	#Funciones para transformar los objetos del sistema
	def rotarObjetos(self, angulo, vector):
		#Creamos el cuaternion de rotación.
		rotacion = Quaternion()
		rotacion.quatRotacion(angulo, vector)

		#Aplicamos el cuaternion a a cada objeto
		for objeto in self.objetos.values():
			#Calculamos el centro del objeto antes de la rotación
			centro = objeto.Centro()
			objeto.Rotar(rotacion)

			#Corregimos la traslacion provocada por la rotacion alineando con el centro anterior
			objeto.Alinear(centro)

	def trasladarObjetos(self, vector):
		#Vector contiene las tres distancias. Usamos * para dividirlo al meterlo como argumento.
		mat = matriz.Trasladar(*vector)
		for objeto in self.objetos.values():
			objeto.Transformar(mat)

		#Escalar.
	def escalarObjetos(self, f, centro):
		mat = matriz.Escalar(f, *centro)
		for objeto in self.objetos.values():
			objeto.Transformar(mat)

	#Centro del sistema
	def Centro(self):
		centros = numpy.zeros((0,3))
		for objeto in self.objetos.values():
			centros = numpy.vstack((centros, objeto.Centro()))

		minC = centros.min(axis = 0)
		maxC = centros.max(axis = 0)

		return (minC + maxC) * 0.5


#--------------------------------------------------------------#
#					   Formas básicas                          #
#--------------------------------------------------------------#

#Vértices y aristas que crean las estructuras básicas
	
	#Prisma rectangular a partir de un punto y unas dimesniones.
def Prisma((x, y, z), (ancho, alto, largo)):
	Prisma = Objeto3D()
	#Los vertices son el punto dado y todos los que salen al añadir las dimensiones
	Prisma.Vertices(numpy.array([(nx, ny, nz) for nx in (x, x + ancho) for ny in (y, y + alto) for nz in (z, z + largo)]))

	#Las caras son las formadas por los vertices en las listas. 
	Prisma.Caras([(0,1,3,2), (7,5,4,6), (4,5,1,0), (2,3,7,6), (0,2,6,4), (5,7,3,1)])
	return Prisma


	#Esferoide a partir de un centro y unos semiejes (rx, ry, rz). El número de vertices viene dado por la resolución.
def Esferoide((x, y, z), (rx, ry, rz), res = 15):
	Esferoide = Objeto3D()
	latitudes = [n*numpy.pi/res for n in xrange(1, res)]
	longitudes = [n*2*numpy.pi/res for n in xrange(res)]

	#Añadimos los vertices. Son los cruces que haya entre las latitudes y las longitudes.
	Esferoide.Vertices([(x + rx*numpy.sin(n)*numpy.sin(m), y - ry*numpy.cos(m), z - rz*numpy.cos(n)*numpy.sin(m)) for m in latitudes for n in longitudes])

	#Añadimos las caras menos en los polos
	numVertices = res * (res - 1)
	Esferoide.Caras([(m+n, (m+res)%numVertices+n, (m+res)%res**2+(n+1)%res, m+(n+1)%res) for n in xrange(res) for m in xrange(0,numVertices-res, res)])

	#Añadimos los vertices y las caras triangulares de los polos
	Esferoide.Vertices([(x, y+ry, z), (x, y-ry, z)])
	Esferoide.Caras([(n, (n+1)%res, numVertices+1) for n in xrange(res)])
	vertInicial = numVertices-res
	Esferoide.Caras([(numVertices, vertInicial+(n+1)%res, vertInicial+n) for n in xrange(res)])

	return Esferoide

	#Plano horizontal. Centro en x, y, z. Dimensiones: dx, dz. Resolucion: Res
def PlanoHorizontal((x,y,z), (dx,dz), Res):
	grid = Objeto3D()
	grid.Vertices([[x+n1*dx, y, z+n2*dz] for n1 in xrange(Res+1) for n2 in xrange(Res+1)])
	grid.Aristas([(n1*(Res+1)+n2,n1*(Res+1)+n2+1) for n1 in xrange(Res+1) for n2 in xrange(Res)])
	grid.Aristas([(n1*(Res+1)+n2,(n1+1)*(Res+1)+n2) for n1 in xrange(Res) for n2 in xrange(Res+1)])
	return grid













