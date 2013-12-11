#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import future
from __future__ import print_function, division

#Import math
import math

#Importamos PyGame para dibujar
import pygame

#Import mis módulos: Clase de vectores y parametros del mundo simulado
from Vector3D import Vector3D
import WorldParams

#Parametros para meter en WorldParams
GRAVITY = 9.8
WORLDFLOOR = 0

#Para el motor de físicas vamos a utilizar objetos esféricos con masa a los que se les puede aplicar una fuerza y uniones rígidas sin masa entre ellos.
class Cuerpo:
	#Constructor
	def __init__(pos, masa, radio, ID):
		self.posicion = Vector3D(pos)
		self.masa = masa
		self.radio = radio
		self.velocidad = Vector3D()
		self.fuerzas = Vector3D()
		self.ID = ID
	#Representación en string de la clase. Para print y debuggear
	def __repr__(self):
		return "ID: %r, Posicion: %r, Velocidad: %r, Fuerzas: %r, Radio: %r, Masa: %r" % (self.ID, self.posicion, self.velocidad, self.fuerzas, self.radio, self.masa)

	#Funciones para actualizar el estado
		#Actualización de posicion
	def Mover(self):
		self.posicion += self.velocidad
		return self

		#Actualizacion de velocidad. Fuerza x Tiempo = Masa * ∆Velocidad ==> ∆Velocidad = Fuerza * Tiempo / Masa
	def Acelerar(self):
		self.velocidad = self.fuerzas * WorldParams.Frame / self.masa
		return self

		#Aplicamos fuerzas sobre el objeto
	def Fuerzas(self, vectorF):
		self.fuerzas = vectorF
		return self

	def Colision(self):


class Uniones:
	#Constructor
	def __init__(self, ID1, ID2, longitud):
		self.inicio = ID1
		self.final = ID2
		self.longitud = longitud







