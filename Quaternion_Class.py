#!/usr/bin/python
# -*- coding: utf-8 -*-

#Importamos future por la compatibilidad
from __future__ import division, print_function

#Importamos math para sqrt
import math

#Importamos Vector3D porque los cuaterniones son vectores con un escalar.
import Vector3D_Class as Vector3D


#--------------------------------------------------------------#
#					   Quaternion class                        #
#--------------------------------------------------------------#

class Quaternion:
	#Constructor
	def __init__(self, a = 0, vx=0, vy=0, vz=0):
		self.escalar = a
		self.vector = Vector3D.Vector3D(vx, vy, vz)

	#Print y debug.
	def __repr__(self):
		return 'Escalar: %r ' % (self.escalar) + Vector3D.Vector3D.__repr__(self.vector)

	#Definimos round para corregir los errores al usar floats. 
	def round(self, n):
		self.escalar = round(self.escalar, n)
		self.vector = self.vector.round(n)
		return self
	#Definimos las operaciones
		#Suma de cuaterniones +=
	def __iadd__(self, other):
			
		self.escalar += other.escalar
		self.vector += other.vector
		return self

		#Suma de cuaterniones +
	def __add__(self, other):
		result = Quaternion(self.escalar, self.vector.x, self.vector.y, self.vector.z)
		result += other
		return result

		#Conjugado de un cuaternion
	def __neg__(self):
		result = Quaternion(self.escalar, -self.vector.x, -self.vector.y, -self.vector.z)
		return result

		#Resta de cuaterniones -=
	def __isub__(self, other):
		self += (-other)
		return self

		#Resta de cuaterniones -
	def __sub__(self, other):
		result = Quaternion(self.escalar, self.vector.x, self.vector.y, self.vector.z)
		result -= other
		return result

		#Multiplicación de un cuaternion por un número *=
	def __imul__(self, other):
		self.escalar *= other
		self.vector *= other
		return self

		#Multiplicación de un cuaternion por un número *
	def __mul__(self, other):
		result = Quaternion(self.escalar, self.vector.x, self.vector.y, self.vector.z)
		result *= other
		return result

	def __rmul__(self, other):
		return self * other

		#División de un cuaternion entre un número /=
	def __itruediv__(self, other):
		self *= (1/other)
		return self

		#División de un cuaternion entre un número /
	def  __truediv__(self, other):
		result = Quaternion(self.escalar, self.vector.x, self.vector.y, self.vector.z)
		result /= other
		return result

	#Definimos la multiplicación de cuaterniones. Q1 = a + v1; Q2 = w + v2; Q1 * Q2 = (a*w - v1 . v2) + (b*v1 + a*v2 + v1 x v2)
	def Mult(self, other):
		result = Quaternion()
		result.escalar = self.escalar * other.escalar - (self.vector.Escalar(other.vector))
		result.vector = self.escalar * other.vector + other.escalar * self.vector + (self.vector.Vectorial(other.vector))
		return result

	#Definimos la conjugación de cuaterniones. Q, P => Cuaterniones. Conjugación: P' = Q * P * Q^(-1)
	#Esta operación es equivalente a rotar el vector P a lo largo de un eje un ángulo definido por Q.
	def Conjugacion(self, other):
		result = Quaternion() 
		other = other.Normalizar()
		result = other.Mult(self)
		result = result.Mult(-other)
		result = result.round(5)
		return result

	#Modulo de un cuaternion
	def Modulo(self):
		return math.sqrt(self.escalar**2 + self.vector.Modulo()**2)

	#Normalización de un cuaternion
	def Normalizar(self):
		return self/self.Modulo()

	#Crear un cuaternión de rotación definido por un ángulo y un vector de aplicación
	def quatRotacion(self, angulo, (vx, vy, vz)):
		self.escalar = round(math.cos(angulo/2), 3)
		self.vector = round(math.sin(angulo/2), 3) * Vector3D.Vector3D(vx, vy, vz)
		self.Normalizar()
		return self

#Test

testQ = Quaternion()
testQ = testQ.quatRotacion(math.pi/2, (1,1,1))
Quat = Quaternion(0,0,0,1)
Quat = Quat.Conjugacion(testQ)
print(Quat)






	

