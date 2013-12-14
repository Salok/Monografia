#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import math
import math

#Importamos PyGame para dibujar
import pygame

#Import mis módulos: Clase de vectores y parametros del mundo simulado
import Display as Disp
import Graphics_Class as Graph
from Vector3D_Class import Vector3D
import WorldParams
import MatrizFunciones as Mat

wp = WorldParams.WorldParams()



#Para el motor de físicas vamos a utilizar objetos esféricos con masa a los que se les puede aplicar una fuerza y uniones rígidas sin masa entre ellos.
class Cuerpo:
	#Constructor
	def __init__(self, pos, masa, radio, ID):
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

		#Actualizacion de velocidad. Fuerza x Tiempo = Masa * ∆Velocidad ==> ∆Velocidad = Fuerza * Tiempo / Masa. Reinicia la fuerza
	def Acelerar(self):
		self.velocidad += self.fuerzas * FRAME_TIME / self.masa
		self.fuerzas = Vector3D()

		#Aplicamos fuerzas sobre el objeto
	def Fuerzas(self, vectorF):
		self.fuerzas += vectorF

	#Función que aplica todas las actualizaciones del objeto.
	def Actualizar(self):
		self.Acelerar()
		self.Mover()

	#Funcion de choque. Intercambia los momentos lineales de los cuerpos que chocan con una pérdida de velocidad
	def Choque(self, other):
		vel = other.velocidad * other.masa / self.masa * wp.COEFICIENTE_ELASTICO
		otherVel = self.velocidad * self.masa / other.masa * wp.COEFICIENTE_ELASTICO

		return (vel, otherVel)

	#Devuelve verdadero si el objeto está en contacto con el suelo
	def contSuelo(self):
		if (self.posicion.y - radio <= WORLDFLOOR):
			self.Fuerzas = Vector3D()
			return true
		else:
			return false







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
		self.objetos3D = Graph.Sistema3D(ID)
		self.masa = 0

	#Representación en string de la clase.
	def __repr__(self):
		debug = 'Soy el sistema %r con masa %r y centro en %r. Estoy compuesto por los cuerpos: \n' % (self.ID, self.masa, self.Centro())
		for ID, cuerpo in self.cuerpos.iteritems():
			debug += Cuerpo.__repr__(cuerpo) + '\n'

		debug += 'Y las uniones: \n'
		for union in self.uniones:
			debug += Union.__repr__(union) + '\n'

		debug += 'Y estoy representado por: \n' + self.objetos3D.__repr__()

		return debug


	#Funciones para añadir elementos al sistema
		#Añadir cuerpos
	def nuevoCuerpo(self, cuerpo):
		self.cuerpos[cuerpo.ID] = cuerpo
		self.masa += cuerpo.masa
		self.objetos3D.nuevoObjeto(cuerpo.ID, cuerpo.objeto3D) 

		#Añadir uniones
	def nuevaUnion(self, union):
		self.uniones.append(union)
		vertices = [(self.cuerpos[union.inicio].posicion.x, self.cuerpos[union.inicio].posicion.y, self.cuerpos[union.inicio].posicion.z), (self.cuerpos[union.final].posicion.x, self.cuerpos[union.final].posicion.y, self.cuerpos[union.final].posicion.z)]
		objeto = Graph.Objeto3D()
		objeto.Vertices(vertices)
		objeto.Aristas([(0, 1)])
		nombre = union.inicio + '-' + union.final
		self.objetos3D.nuevoObjeto(nombre, objeto)

	#Calcula el centro de masas del sistema
	def Centro(self):
		numCuerpos = len(self.cuerpos.values())

		calculo = Vector3D()

		if (numCuerpos != 0):
			for cuerpo in self.cuerpos.values():
				calculo += cuerpo.masa * cuerpo.posicion

			calculo /= numCuerpos

		return calculo

	#Actualiza todos los cuerpos del sistema
	def Actualizar(self, fuerzaExt = Vector3D()):
		Colsion()
		for cuerpo in self.cuerpos.values():
			self.Fuerzas(fuerzaExt)
			cuerpo.Actualizar()


	#Comprobamos si los cuerpos de un sistema están chocando y corregimos su posición si lo hacen.
	def Colision(self):
		for i, cuerpo1 in enumerate(self.cuerpos.values()):
			for j, cuerpo2 in enumerate(self.cuerpos.calues()[i+1:]):
				distancia = Vector3D.Modulo(cuerpo1.posicion - cuerpo2.posicion) - cuerpo1.radio - cuerpo2.radio
				if (distancia <= 0):
					normDist = Vector3D.Normalizar(cuerpo1.posicion - cuerpo2.posicion)
					cuerpo1.pos += distancia/2 * normDist
					cuerpo2.pos -= distancia/2 * normDist
					cuerpo1.velocidad, cuerpo2.velocidad = cuerpo1.Choque(cuerpo2)

	
	#Transmite las fuerzas entre los objetos unidos
	def Transmision(self):
		for union in self.uniones:
			#Creamos un vector de transmisión de fuerzas. Es el vector unitario de la recta de la unión
			vectTrans = Vector3D.Normalize(self.cuerpos[union.inicio].posicion-self.cuerpos[union.final].posicion)
			#Las fuerzas paralelas al vector de transmisión son las que pasan de un cuerpo a otro.
			#Para calcularlas utilizamos el producto escalar. ==> v1 . v2 = |v1||v2|cos(ang)   |v2| = 1 ===> |v1|.cos(ang) 
			fuerza1 = vecTrans * (self.cuerpos[union.inicio].fuerzas.Escalar(vecTrans))
			fuerza2 = -vecTrans * (self.cuerpos[union.final].fuerzas.Escalar(-vecTrans))

			self.cuerpos[union.inicio].fuerzas += fuerza1
			self.cuerpos[union.final].fuerzas += fuerza2



class Mundo:

	#Constructor
	def __init__(self):
		self.pantalla = Disp.Proyector(wp.ANCHO_PANTALLA, wp.ALTO_PANTALLA)
		self.sistemas = {}

	def __repr__(self):
		debug = 'Soy el mundo. Tengo los sistemas: \n'


		for sistema in self.sistemas.values():
			debug += sistema.__repr__() + '\n'

		debug += self.pantalla.__repr__()

		return debug

	def nuevoSistema(self, sistema):
		self.sistemas[sistema.ID] = sistema
		self.pantalla.nuevoSisObjetos(sistema.objetos3D)


mundo = Mundo()
sistema = Sistema('1')
cuerpo1 = Cuerpo((50, 50, 50), 1, 50, '1')
cuerpo2 = Cuerpo((250, 50, 50), 1, 50, '2')
union = Union('1', '2', 200)
sistema.nuevoCuerpo(cuerpo1)
sistema.nuevoCuerpo(cuerpo2)
sistema.nuevaUnion(union)
sistema2 = Sistema('2')
cuerpo3 = Cuerpo((50, 150, 50), 1, 50, '3')
cuerpo4 = Cuerpo((250, 150, 50), 1, 50, '4')
union2 = Union('3', '4', 200)
sistema2.nuevoCuerpo(cuerpo3)
sistema2.nuevoCuerpo(cuerpo4)
sistema2.nuevaUnion(union2)
mundo.nuevoSistema(sistema)
mundo.nuevoSistema(sistema2)
for sistema in mundo.sistemas.values():
	print(sistema.objetos3D.ID)

print(mundo.pantalla.sistemas.keys())
mundo.pantalla.dibPantalla()















