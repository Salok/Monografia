#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import Numpy para trabajar con matrices
import numpy

#Importamos los cuaterniones para rotar objetos
import Quaternion_Class as Quat

#--------------------------------------------------------------#
#					   Objeto3D class                          #
#--------------------------------------------------------------#

#Los objetos son grupos de vertices y aristas
class Objeto3D:
	#Constructor. Guarda una lista con los vertices y otra con las aristas. También guarda el número de aristas y el de vertices.
	def __init__(self):
		self.vertices = numpy.zeros((0, 4))
		self.aristas = []

	#Representación en string de la clase. Para print y debuggear
	def __repr__(self):
		verticesDebug = "\n --- Vertices --- \n"
		for i, (x, y , z, _) in enumerate(self.vertices):
			verticesDebug += "Vertice %d: %d, %d, %d \n" % (i, x, y, z)

		aristasDebug = "\n --- Aristas --- \n"
		for i, (ver1, ver2) in enumerate(self.aristas):
			aristasDebug += "Arista %d: Une los vertices %d y %d \n" % (i, ver1, ver2)

		#Lo juntamos todo y lo devolvemos.
		final = ('Tengo %r vertices que son: \n' + verticesDebug + 'y %r aristas que son: \n' + aristasDebug) % (len(self.vertices), len(self.aristas))
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

	#Aplicar una matriz de transformación
	def Transformar(self, mat):
		self.vertices = numpy.dot(self.vertices, mat)

	#Rotar el objeto con un cuaternión
	def Rotar(self, qRotacion):
		#Aplicamos el cuaternión a cada uno de los vertices del objeto
		for i, (x, y, z, _) in enumerate(self.vertices):
			rotado = Quat.Quaternion(0, x, y, z).Conjugacion(qRotacion)
			self.vertices[i] = [rotado.vector.x, rotado.vector.y, rotado.vector.z, 1]









