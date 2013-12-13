#!/usr/bin/python
# -*- coding: utf-8 -*-

#Importamos future por la compatibilidad
from __future__ import division, print_function

#Importamos math
import math

#Importamos Numpy para las operaciones con matrices
import numpy


#--------------------------------------------------------------#
#			        Funciones de matrices                      #
#--------------------------------------------------------------#
#Crea una matriz de transformación que traslada un punto unas distancias dx, dy y dz.
def Trasladar(dx, dy, dz):
	return numpy.array([[1, 0, 0, 0],
					 [0, 1, 0, 0],
					 [0, 0, 1, 0],
					 [dx,dy,dz,1]])

#Crea una matriz de transformación que escala un punto en un factor f desde un centro cx, cy, cz
def Escalar(f, cx, cy, cz):
    return numpy.array([[f,0,0,0],
                     [0,f,0,0],
                     [0,0,f,0],
                     [cx*(1-f), cy*(1-f), cz*(1-f), 1]])








