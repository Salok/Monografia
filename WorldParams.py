#!/usr/bin/python
# -*- coding: utf-8 -*-

#Clase para incluir parametros del mundo como la gravedad, la eslasticidad de los materiales, la resistencia del aire, las fuerzas máximas...

class WorldParams:
	#Constructor
	def __init__(self):
		#Parametros del display
		self.NEGRO = (0, 0, 0)
		self.BLANCO = (255, 255, 255)
		self.DIBUJAR_VERTICES = False
		self.DIBUJAR_ARISTAS = True
		self.COLOR_VERTICES = (255, 255, 255)
		self.COLOR_ARISTAS = (200, 200, 200)
		self.RADIO_VERTICES = 5
		self.ANCHO_PANTALLA = 600
		self.ALTO_PANTALLA = 450

		#Parametros de Física
		self.GRAVITY = 9.81
		self.WORLDFLOOR = 0
		self.MASS_SPHERE = 1
		self.RADIUS_SPHERE = 50
		self.FRAME_TIME = 1/25
		self.COEFICIENTE_ELASTICO = 0.5