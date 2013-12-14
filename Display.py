#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import pygame para dibujar y numpy para mates
import pygame, numpy

#Import mis módulos: Clase de vectores, clase de graficos y funciones de matrices
from Quaternion_Class import Quaternion
from Vector3D_Class import Vector3D
import Graphics_Class as Graph
import MatrizFunciones as matriz
import WorldParams

wp = WorldParams.WorldParams()

#--------------------------------------------------------------#
#					   Proyector class                         #
#--------------------------------------------------------------#

#Clase que guarda los objetos y tiene todas las variables necesarias para dibujarlos
class Proyector:
	#Constructor
	def __init__(self, xmax, ymax):
		#Tamaño de la pantalla
		self.xMax = xmax
		self.yMax = ymax

		#Pantalla de pygame
		self.pantalla = pygame.display.set_mode((xmax, ymax))
		pygame.display.set_caption('Proyector3D')
		self.colorFondo = wp.NEGRO 

		#Diccionario con los objetos
		self.sistemas = {}

		#Sistema sobre el que se aplican las transformaciones
		self.sistElegido = '1'

		#Condiciones de dibujo
		self.dibVertices = wp.DIBUJAR_VERTICES
		self.dibAristas = wp.DIBUJAR_ARISTAS
		self.colorVertices = wp.COLOR_VERTICES
		self.colorAristas = wp.COLOR_ARISTAS
		self.radioVertices = wp.RADIO_VERTICES

	def __repr__(self):
		debug = 'Mi pantalla es de %r de ancho y %r de alto. \n El color de fondo es %r. \n El color de las aristas es: %r. \n' % (self.xMax, self.yMax, self.colorFondo, self.colorAristas )
		debug += 'El color de los vertices es: %r.\n El tamaño de los vertices es %r. \n Dibujando Vertices: %r. \n Dibujando Aristas: %r.\n' % (self.colorVertices, self.radioVertices, self.dibVertices, self.dibAristas)
		#Recogemos el mensaje de debug de cada una de las aristas
		for nombre, objeto in self.objetos.iteritems():
			debug += ('Soy el objeto %r: ' % (nombre) + Graph.Objeto3D.__repr__(objeto))
			debug += '\n'

		return debug


	#Mantiene una pantalla de pygame dibujada mientras este abierto el programa
	def dibPantalla(self):
		abierto = True
		while abierto:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					abierto = False
				elif event.type == pygame.KEYDOWN:
					if event.key in key_to_function.keys():
						key_to_function[event.key](self)

			#self.rotarObjetos(numpy.pi/180, (1,1,1))
			self.pantalla.fill(self.colorFondo)
			self.dibObjetos()
			pygame.display.flip()

	#Añadimos un nuevo sistema de objeto con nombre para poder tratarlo individualmente.
	def nuevoSisObjetos(self, sistema):
		self.sistemas[sistema.ID] = sistema



	#Funcion que dibuja los objetos del diccionario
	def dibObjetos(self):
		#Por cada sistema en el proyector
		for sistema in self.sistemas.values():
		#Si dibujamos los vertices...
			for objeto in sistema.objetos.values():
				if self.dibVertices:
					# Por cada vertices
					for vertice in objeto.vertices:
						#Lo dibujamos en sus coordenadas en x e y
						pygame.draw.circle(self.pantalla, self.colorVertices, (int(vertice[0]), int(vertice[1])), self.radioVertices, 0)

				#Si dibujamos las aristas...
				if self.dibAristas:
					#Por cada arista
					for ver1, ver2 in objeto.aristas:
						#Dibujamos una línea entre su inicio y su final
						pygame.draw.aaline(self.pantalla, self.colorAristas, objeto.vertices[ver1][:2], objeto.vertices[ver2][:2], 1)

	#Funciones de transformación globales. Transforman todos los objetos del proyector
		#Trasladar.
	def trasladarSistema(self, vector):
		#Vector contiene las tres distancias. Usamos * para dividirlo al meterlo como argumento.
		self.sistemas[self.sistElegido].trasladarObjetos(vector)

		#Escalar.
	def escalarSistema(self, f, centro):
		self.sistemas[self.sistElegido].escalarObjetos(f, centro)

		#Rotar
	def rotarSistema(self, angulo, vector):
		self.sistemas[self.sistElegido].rotarObjetos(angulo, vector)

	def elegirSistema(self, ID):
		self.sistElegido = ID



#Test: Display
#Test: Cube
#Test: Transformations
key_to_function = {
	pygame.K_LEFT: 	(lambda x: x.trasladarSistema([-10, 0, 0])),
	pygame.K_RIGHT:	(lambda x: x.trasladarSistema([ 10, 0, 0])),
	pygame.K_DOWN: 	(lambda x: x.trasladarSistema([0,  10, 0])),
	pygame.K_UP:   	(lambda x: x.trasladarSistema([0, -10, 0])),
	pygame.K_q:    	(lambda x: x.escalarSistema(2, [wp.ANCHO_PANTALLA/2, wp.ALTO_PANTALLA/2, 0])),
 	pygame.K_e:    	(lambda x: x.escalarSistema(0.5, [wp.ANCHO_PANTALLA/2, wp.ALTO_PANTALLA/2, 0])),
 	pygame.K_a:	   	(lambda x: x.rotarSistema(numpy.pi/4, (1,0,0))),
 	pygame.K_s:	   	(lambda x: x.rotarSistema(numpy.pi/4, (0,1,0))),
 	pygame.K_d:	   	(lambda x: x.rotarSistema(numpy.pi/4, (0,0,1))),
 	 pygame.K_z:	(lambda x: x.rotarSistema(numpy.pi/4, (1,0,0))),
 	pygame.K_x:	   	(lambda x: x.rotarSistema(numpy.pi/4, (0,1,0))),
 	pygame.K_c:	   	(lambda x: x.rotarSistema(numpy.pi/4, (0,0,1))),
 	pygame.K_1:		(lambda x: x.elegirSistema('1')),
 	pygame.K_2:		(lambda x: x.elegirSistema('2'))
 }




