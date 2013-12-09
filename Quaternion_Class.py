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
		return 'Escalar: %r' % (self.escalar) + Vector3D.Vector3D.__repr__(self.vector)

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
		result = Quaternion(self.escalar, -self.vector)
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

	#Definimos la multiplicación de cuaterniones. Q1 = a + v1; Q2 = w + v2; Q1 * Q2 = (a*w - v1 . v2) + (a*v1 + b*v2 + v1 x v2)
	def Mult(self, other):
		result = Quaternion(self.escalar, self.vector.x, self.vector.y, self.vector.z)
		result.escalar *= other.escalar  
		result.escalar -= result.vector.Escalar(other.vector)
		result.vector = (result.escalar * result.vector) + (other.escalar * other.vector) + (result.vector.Vectorial(other.vector))
		return result

	#Definimos la conjugación de cuaterniones. Q, P => Cuaterniones. Conjugación: P' = Q * P * Q^(-1)
	#Esta operación es equivalente a rotar el vector P a lo largo de un eje un ángulo definido por Q.
	def Conjugacion(self, other):
		result = Quaternion() 
		result += other * self * -other
		return result

	#Modulo de un cuaternion
	def Modulo(self):
		return math.sqrt(self.escalar**2 + self.vector.Modulo()**2)

	#Normalización de un cuaternion
	def Normalizar(self):
		return self/self.Modulo()

	#Crear un cuaternión de rotación definido por un ángulo y un vector de aplicación
	def quatRotacion(self, angulo, (vx, vy, vz)):
		self.escalar = math.cos(angulo)/2
		self.vector = math.sin(angulo)/2 * Vector3D.Vector3D(vx, vy, vz)
		self.Normalizar()
		return self

#Test

testQ = Quaternion()
testQ = testQ.quatRotacion(2*math.pi/3, (1,1,1))
testV = Quaternion(0,1,1,1)
testW = Quaternion(0,0,0,1)
print("Quaternions: \n")
print(testQ)
print(testV)
print(testW)
final = testW.Mult(testV)
print("W * V \n")
print(final)
final = testV.Mult(testW)
print("V * W \n")
print(final)
final = testV.Conjugacion(testQ)
print("Conjugado de V y Q: V rotado 90 grados \n")
print(final)
final = testW.Conjugacion(testQ)
print("Conjugado de W y Q: W rotado 90 grados \n")
print(final)





	

