#!/usr/bin/python
# -*- coding: utf-8 -*-

#Importamos future por la compatibilidad
from __future__ import division, print_function

#Importamos math
import math

#Importamos Numpy para las operaciones con matrices
import numpy as np


#--------------------------------------------------------------#
#			        Funciones de matrices                      #
#--------------------------------------------------------------#
#Crea una matriz de transformación que traslada un punto unas distancias dx, dy y dz.
def Trasladar(dx, dy, dz):
	return np.array([[1, 0, 0, 0],
					 [0, 1, 0, 0],
					 [0, 0, 1, 0],
					 [dx,dy,dz,1]])

#Crea una matriz de transformación que escala un punto en unos factores fx, fy y fz
def Escalar(fx, fy, fz):
	return np.array([[fx, 0, 0, 0],
					 [0, fy, 0, 0],
					 [0, 0, fz, 0],
					 [0, 0, 0,  1]])








