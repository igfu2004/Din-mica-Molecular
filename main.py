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
numero_discos = 6
masa = 1
radio = 0.1
velomax = 0.1

############################### Creacion de los elementos del sistema ##################################
discos = []

caja = Box(ladohorizontal, ladovertical)

grilla = Grilla(caja.longitudx,caja.longitudy,radio)

discos = inicializacion_discos(radio, masa, -velomax, velomax, grilla, numero_discos, True, True)

######################################## Evolucion del sistema #########################################

FPS = 60
newt = 1/FPS
tmax = 60
tprima = 0
timearray = np.zeros(tmax*FPS)
fotograma = 0

for n in range(0,tmax*FPS):
    #actualizacion de posiciones
    #tprima es el tiempo actual del sistema
    tprima = n*newt
    timearray[n] = tprima
    #actualizacion de las posiciones de los discos
    for i in range(numero_discos):
        discos[i] = nueva_posicion(discos[i],newt)
        #verificación de colisiones con las paredes
        discos[i] = deteccion_colision_pared(discos[i],caja.longitudx,caja.longitudy,newt)
    #verificacion de colisiones entre los discos
    discos = deteccion_colision_pares(grilla,discos,cambio_velocidad_colision_pares,n,newt,sistema_colision_forzada_pares)
    graf_discos(discos,caja,fotograma,grilla)
    fotograma += 1

crear_video(FPS)

histo_discos(discos,timearray,tmax,newt)
