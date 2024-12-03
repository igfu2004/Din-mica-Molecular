#!/usr/bin/env python3
from clases import Disco, Box, Grilla
from funciones import *
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf
from moviepy.editor import *
import glob
import os

################################### Parámetros iniciales del sistema ###################################
#dimensiones de la caja
ladohorizontal = 1
ladovertical = 1

#parametros de los discos
numero_discos = 200
masa = 1
radio = 0.01
velomax = 0.1

#tiempo de simulacion en segundos
tmax = 60

############################### Creacion de los elementos del sistema ##################################
discos = []

caja = Box(ladohorizontal, ladovertical)

grilla = Grilla(caja.longitudx,caja.longitudy,radio)

discos = inicializacion_discos(radio, masa, -velomax, velomax, grilla, numero_discos, True, True)

######################################## Evolucion del sistema #########################################

FPS = 60
newt = 1/FPS

fotograma = 0

for n in range(0,tmax*FPS):
    #actualizacion de las posiciones de los discos
    for i in range(numero_discos):
        discos[i] = nueva_posicion(discos[i],newt)

    #Verificacion de colisiones
    discos = colision_proxima(grilla,discos,cambio_velocidad_colision_pares,newt,manejo_de_colisiones_pares,tiempo_colision_pared,deteccion_colision_pared_con_manejo,caja.longitudx,caja.longitudy)

    #graf_discos(discos,caja,fotograma,grilla)
    #fotograma += 1

#crear_video(FPS)

#Creacion del histograma
histo_discos(discos,caja.longitudx,50)
