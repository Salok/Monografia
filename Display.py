#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import pygame para dibujar y numpy para mates
import pygame, numpy

#Import mis módulos: Clase de vectores, clase de graficos y funciones de matrices
import Quaternion_Class as Quat
from Vector3D_Class import Vector3D
import Graphics_Class as Graph
import MatrizFunciones as matriz

#Parametros para WorldParams
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
DIBUJAR_VERTICES = True
DIBUJAR_ARISTAS = True
COLOR_VERTICES = (255, 255, 255)
COLOR_ARISTAS = (200, 200, 200)
RADIO_VERTICES = 5
ANCHO_PANTALLA = 600
ALTO_PANTALLA = 450

#--------------------------------------------------------------#
#					   Proyector class                         #
#--------------------------------------------------------------#

#Clase que guarda los objetos y tiene todas las variables necesarias para dibujarlos
class proyector:
	#Constructor
	def __init__(self, xmax, ymax):
		#Tamaño de la pantalla
		self.xMax = xmax
		self.yMax = ymax

		#Pantalla de pygame
		self.pantalla = pygame.display.set_mode((xmax, ymax))
		pygame.display.set_caption('Proyector3D')
		self.colorFondo = NEGRO 

		#Diccionario con los objetos
		self.objetos = {}

		#Condiciones de dibujo
		self.dibVertices = DIBUJAR_VERTICES
		self.dibAristas = DIBUJAR_ARISTAS
		self.colorVertices = COLOR_VERTICES
		self.colorAristas = COLOR_ARISTAS
		self.radioVertices = RADIO_VERTICES

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

			self.pantalla.fill(self.colorFondo)
			self.dibObjetos()
			pygame.display.flip()

	#Añadimos un nuevo objeto con nombre para poder tratarlo individualmente.
	def nuevoObjeto(self, nombre, objeto):
		self.objetos[nombre] = objeto

	#Funcion que dibuja los objetos del diccionario
	def dibObjetos(self):
		#Por cada objeto en el pryector
		for objeto in self.objetos.values():	
			#Si dibujamos los vertices...
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

	#Funciones de transformación globales. Transofrman todos los objetos del proyector
		#Trasladar.
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

		#Rotar
	def rotarObjetos(self, angulo, vector):
		#Creamos el cuaternion de rotación.
		rotacion = Quat.Quaternion()
		rotacion.quatRotacion(angulo, vector)

		#Aplicamos el cuaternion a a cada objeto
		for objeto in self.objetos.values():
			objeto.Rotar(rotacion)



#Test: Display
#Test: Cube
#Test: Transformations
key_to_function = {
	pygame.K_LEFT: (lambda x: x.trasladarObjetos([-10, 0, 0])),
	pygame.K_RIGHT:(lambda x: x.trasladarObjetos([ 10, 0, 0])),
	pygame.K_DOWN: (lambda x: x.trasladarObjetos([0,  10, 0])),
	pygame.K_UP:   (lambda x: x.trasladarObjetos([0, -10, 0])),
	pygame.K_q:    (lambda x: x.escalarObjetos(2, [ANCHO_PANTALLA/2, ALTO_PANTALLA/2, 0])),
 	pygame.K_e:    (lambda x: x.escalarObjetos(0.5, [ANCHO_PANTALLA/2, ALTO_PANTALLA/2, 0])),
 	pygame.K_x:	   (lambda x: x.rotarObjetos(numpy.pi/4, (1,0,0))),
 	pygame.K_y:	   (lambda x: x.rotarObjetos(numpy.pi/4, (0,1,0))),
 	pygame.K_z:	   (lambda x: x.rotarObjetos(numpy.pi/4, (0,0,1)))
 }

cubo = Graph.Objeto3D()
vertices = numpy.array([(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)])
cubo.Vertices(vertices)
cubo.Aristas([(n,n+4) for n in range(0,4)]+[(n,n+1) for n in range(0,8,2)]+[(n,n+2) for n in (0,1,4,5)])
pv = proyector(ANCHO_PANTALLA, ALTO_PANTALLA)
pv.nuevoObjeto("cubo", cubo)
print(pv)
pv.dibPantalla()




