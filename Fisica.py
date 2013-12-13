#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import math
import math

#Importamos PyGame para dibujar
import pygame

#Import mis módulos: Clase de vectores y parametros del mundo simulado
import Graphics_Class as Graph
from Vector3D import Vector3D
import WorldParams
import MatrizFunciones as Mat

#Parametros para meter en WorldParams
GRAVITY = 9.81
WORLDFLOOR = 0
MASS_SPHERE = 1
RADIUS_SPHERE = 50
FRAME_TIME = 1/25



#Para el motor de físicas vamos a utilizar objetos esféricos con masa a los que se les puede aplicar una fuerza y uniones rígidas sin masa entre ellos.
class Cuerpo:
	#Constructor
	def __init__(pos, masa, radio, ID):
		self.posicion = Vector3D(*pos)
		self.masa = masa
		self.radio = radio
		self.velocidad = Vector3D()
		self.fuerzas = Vector3D()
		self.objeto3D = Graph.Esferoide(pos, (radio, radio, radio))
		self.ID = ID
	#Representación en string de la clase. Para print y debuggear
	def __repr__(self):
		return "ID: %r, Posicion: %r, Velocidad: %r, Fuerzas: %r, Radio: %r, Masa: %r" % (self.ID, self.posicion, self.velocidad, self.fuerzas, self.radio, self.masa)

	#Funciones para actualizar el estado
		#Actualización de posicion
	def Mover(self):
		self.posicion += self.velocidad
		mat = Mat.Trasladar(*self.velocidad)
		self.objeto3D.Transformar(mat)

		#Actualizacion de velocidad. Fuerza x Tiempo = Masa * ∆Velocidad ==> ∆Velocidad = Fuerza * Tiempo / Masa
	def Acelerar(self):
		self.velocidad += self.fuerzas * FRAME_TIME / self.masa

		#Aplicamos fuerzas sobre el objeto
	def Fuerzas(self, vectorF):
		self.fuerzas += vectorF

	#Función que aplica todas las actualizaciones del objeto.
	def Actualizar(self, fuerzaExt):
		self.Fuerzas(fuerzaExt)
		self.Acelerar()
		self.Mover()





#Representan las uniones entre las esferas que forman los sistemas. Los ID's indican las esferas que unen y la longitud es la que debe haber siempre
#entre ellas.
class Union:
	#Constructor
	def __init__(self, ID1, ID2, longitud):
		self.inicio = ID1
		self.final = ID2
		self.longitud = longitud

	def __repr__(self):
		return 'Union entre los cuerpos %r y %r de longitud %r' % (self.inicio, self.final, self.longitud)

#El sistema de objetos es la representación de cada uno de los individuos o conjuntos de objetos afectados por la física.
class Sistema:
	#Constructor
	def __init__(self, ID):
		self.ID = ID
		self.cuerpos = {}
		self.uniones = []
		self.objetos3D = Graph.Sistema3D
		self.masa = 0

	#Representación en string de la clase.
	def __repr__(self):
		debug = 'Soy el sistema %r con centro en %r. Estoy compuesto por los cuerpos: \n' % (self.ID, self.Centro())
		for ID, cuerpo in self.cuerpos.itervalues():
			debug += Cuerpo.__repr__(cuerpo) + '\n'

		debug += 'Y las uniones: \n'
		for union in self.uniones:
			debug += Union.__repr__(union) + '\n'

		return debug

	#Funciones para añadir elementos al sistema
		#Añadir cuerpos
	def nuevoCuerpo(self, cuerpo):
		if (cuerpo.ID not in self.cuerpos.keys()):
			self.cuerpos[cuerpo.ID] = cuerpo
			self.masa += cuerpo.masa
			self.objetos3D.nuevoObjeto(cuerpo.ID, cuerpo.objeto3D) 

		#Añadir uniones
	def nuevaUnion(self, union):
		if (union not in self.uniones):
			self.uniones += union

	#Calcula el centro de masas del sistema
	def Centro(self):
		numCuerpos = len(self.cuerpos.values())

		calculo = Vector3D()

		if (numCuerpos != 0)
			for cuerpo in self.cuerpos.values():
				calculo += cuerpo.masa * cuerpo.posicion

			calculo /= numCuerpos

		return calculos

	#Actualiza todos los cuerpos del sistema
	def Actualizar(self, fuerzaExt = Vector3D()):
		for cuerpo in self.cuerpos.values():
			cuerpo.Actualizar(fuerzaExt)








class Mundo:















