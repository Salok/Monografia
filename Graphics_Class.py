#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import Numpy para trabajar con matrices
import numpy


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
		unoCol = numpy.ones((len(listaVertices), 1))
		add = numpy.hstack((listaVertices, unoCol))
		self.vertices = numpy.vstack((self.vertices, add))

	#Coge una lista de indices de vertices y las convierte en aristas para añadir al objeto
	def Aristas(self, listaAristas):
		self.aristas += listaAristas

	#Aplicar una matriz de transformación
	def Transformar(self, mat):
		self.vertices = numpy.dot(self.vertices, mat)









