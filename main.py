#!/usr/bin/env python3
from modelo import Disco, Box, Grilla
from controlador import *
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf
from moviepy.editor import *
import glob
import os

ladohorizontal = 1
ladovertical = 1
caja = Box(ladohorizontal,ladovertical)

discos = []
numero_discos = 6
masa = 1
radio = 0.05
velomax = 0.1

discos = acomodo_inicial_discos(radio, masa, -velomax, velomax, caja, numero_discos, True)

grilla = Grilla(caja.longitudx,caja.longitudy,discos)

FPS = 60
newt = 1/FPS
tmax = 5
tprima = 0
timearray = np.zeros(tmax*FPS)
fotograma = 0

for n in range(0,tmax*FPS):
    tprima = n*newt
    timearray[n] = tprima

    for i in range(numero_discos):
        discos[i] = nueva_posicion(discos[i],newt)
        discos[i] = deteccion_colision_pared(discos[i],caja.longitudx,caja.longitudy,newt)
    discos = deteccion_colision_pares(grilla,discos,cambio_velocidad_colision_pares,n,newt,sistema_colision_forzada_pares)
    graf_discos(discos,caja,fotograma,grilla)
    fotograma += 1

crear_video(FPS)

histo_discos(discos,timearray,tmax,newt)
