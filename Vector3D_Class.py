#!/usr/bin/python
# -*- coding: utf-8 -*-

#Importamos future por la compatibilidad
from __future__ import division, print_function

#Importamos math para sqrt
import math

#Incluye vectores y cuaterniones.

#--------------------------------------------------------------#
#					   Vector3D class                          #
#--------------------------------------------------------------#
class Vector3D:

	#Constructor del vector
	def __init__(self, a = 0, b = 0, c = 0):
		self.x = a
		self.y = b 
		self.z = c
	#Representacion en string de la clase. Para print y para debuggear
	def __repr__(self):
		return "x = %r, y = %r, z = %r" % (self.x, self.y, self.z)


	#Definimos round para corregir los errores al trabajar con floats
	def round(self, n):
		self.x = round(self.x, n)
		self.y = round(self.y, n)
		self.z = round(self.z, n)
		return self
	#Definimos las operaciones
		#Suma de vectores +=
	def __iadd__(self, other):
		self.x += other.x
		self.y += other.y
		self.z += other.z
		return self

		#Suma de vectores +
	def __add__(self, other):
		result = Vector3D(self.x, self.y, self.z)
		result += other
		return result

		#Opuesto de un vector
	def __neg__(self):
		result = Vector3D(-self.x, -self.y, -self.z)
		return result

		#Resta de vectores -=
	def __isub__(self, other):
		self += (-other)
		return self

		#Resta de vectores -
	def __sub__(self, other):
		result = Vector3D(self.x, self.y, self.z)
		result -= other
		return result

		#Multiplicación de un vector por un número *=
	def __imul__(self, other):
		self.x *= other
		self.y *= other
		self.z *= other
		return self

		#Multiplicación de un vector por un número *
	def __mul__(self, other):
		result = Vector3D(self.x, self.y, self.z)
		result *= other
		return result

	def __rmul__(self, other):
		return self * other
		return self

		#División de un vector entre un número /=
	def __itruediv__(self, other):
		self *= (1/other)
		return self

		#División de un vector entre un número /
	def  __truediv__(self, other):
		result = Vector3D(self.x, self.y, self.z)
		result /= other
		return result

	#Funciones de operaciones propias de vectores
	#Modulo de un vector
	def Modulo(self):
		return math.sqrt(self.x**2 + self.y**2 + self.z**2)

	#Devuelve el vector normalizado
	def Normalizar(self):
		return self/self.Modulo()

	#Devuelve el producto escalar de dos vectores
	def Escalar(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	#Devuelve el producto vectorial de dos vectores
	def Vectorial(self, other):
		result = Vector3D()
		result.x = self.y * other.z - other.y * self.z
		result.y = self.z * other.x - other.z * self.x
		result.z = self.x * other.y - other.x * self.y
		return result





























