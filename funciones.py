#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf
from random import randint as ri
from moviepy.editor import *
import glob
from clases import Disco, Box, Grilla

def nueva_posicion(disco, dt):
    #funcion para una nueva posicion del disco al moverse
    #con la ec. x_f = x_0 + vt
    posxFinal = disco.posicionx + disco.velocidad[0] * dt
    posyFinal = disco.posiciony + disco.velocidad[1] * dt

    disco.posicionx = posxFinal
    disco.posiciony = posyFinal

    disco.arrayposicionx = np.append(disco.arrayposicionx,posxFinal)
    disco.arrayposiciony = np.append(disco.arrayposiciony,posyFinal)
    return disco
def deteccion_colision_pared(disco,lx,ly,newt):
  
  #Esta parte viene de realizar una parametrización de la trayectoria del disco por medio de la ecuación paramétrica de la recta.
  #Buscamos el tiempo t entre el intervalo de [0,1] en el que se causa la colisión con la pared

  posicioninicial = disco.right()
  posicionfinal = disco.right() + disco.velocidad[0]*newt
  if posicionfinal >= lx:
    t = (lx - disco.right())/(posicionfinal - disco.right())
    x = disco.right() + t*(posicionfinal-disco.right())
    disco.posicionx = x - disco.radio
    disco.velocidad[0] *= -1

  posicioninicial = disco.left()
  posicionfinal = disco.left() + disco.velocidad[0]*newt
  if posicionfinal <= 0:
    t = -1*disco.left()/(posicionfinal - disco.left())
    x = disco.left() + t*(posicionfinal-disco.left())
    disco.posicionx = x + disco.radio
    disco.velocidad[0] *= -1

  posicioninicial = disco.top()
  posicionfinal = disco.top() + disco.velocidad[1]*newt
  if posicionfinal >= ly:
    t = (ly - disco.top())/(posicionfinal - disco.top())
    y = disco.top() + t*(posicionfinal-disco.top())
    disco.posiciony = y - disco.radio
    disco.velocidad[1] *= -1

  posicioninicial = disco.bottom()
  posicionfinal = posicioninicial + disco.velocidad[1]*newt
  if posicionfinal <= 0:
    t = -1*disco.bottom()/(posicionfinal - disco.bottom())
    y = disco.bottom() + t*(posicionfinal - disco.bottom())
    disco.posiciony = y + disco.radio
    disco.velocidad[1] *= -1

  return disco


def cambio_velocidad_colision_pares(disco1,disco2):
  #Buscamos el vector entre el centro de los discos
  n = np.array([disco2.posicionx - disco1.posicionx, disco2.posiciony - disco1.posiciony])

  #Normalizammos el vector:
  nu = n/np.linalg.norm(n)

  #Buscamos el vector tangente unitario a los discos, el cual es perpendicular al vector normal.
  vect = np.array([-1*nu[1],-nu[0]])

  #Buscamos el componente paralelo a nu y vect de las velocidades iniciales, para asi tenerlos en terminos de nu y vect

  v1n = np.dot(disco1.velocidad, nu)
  v2n = np.dot(disco2.velocidad, nu)
  v1t = np.dot(disco1.velocidad, vect)
  v2t = np.dot(disco2.velocidad, vect)

  #notese que al haber hecho el analisis anterior, la colision queda como de una sola dimension, puesto que lo que se esta
  #haciendo es hacer un cambio de sistema de coordenadas realmente, para asi tener que los componentes de la velocidad involucrados
  #en la colision sean en una sola dimension, y asi aplicar la siguiente formula.

  v1nfinal = (v1n*(disco1.masa - disco2.masa) + 2*disco2.masa*v2n)/(disco1.masa + disco2.masa)
  v2nfinal = (v2n*(disco2.masa - disco1.masa) + 2*disco1.masa*v1n)/(disco1.masa + disco2.masa)

  #Estos valores son escalares, por lo que buscamos las proyecciones sobre los vectores nu y vect

  v1nPrima = v1nfinal*nu
  v2nPrima = v2nfinal*nu
  v1tPrima = v1t*vect
  v2tPrima = v2t*vect

  #Por ultimo, nos queda un vector final que es la suma de los vectores paralelos a nu y vect que esta en sistema de coordenadas cartesiano

  v1Prima = v1nPrima + v1tPrima
  v2Prima = v2nPrima + v2tPrima

  disco1.velocidad[0] = v1Prima[0]
  disco1.velocidad[1] = v1Prima[1]
  disco2.velocidad[0] = v2Prima[0]
  disco2.velocidad[1] = v2Prima[1]

  return disco1, disco2


def deteccion_colision_pares(grilla,ldiscos,cambio_velocidad,n,newt,manejo_colision):
  
  #verificación de posiciones en un grilla y en sus vecinas inmediatas sobre el eje x
  for j in grilla.divisionX:
    discos_en_grilla = []
    for i in range(len(ldiscos)):
      if abs(ldiscos[i].posicionx - j) < (2*grilla.dist_entre_separX):
          discos_en_grilla.append(ldiscos[i])

    for i in discos_en_grilla:
      for k in discos_en_grilla:
        if i == k:
          pass
        else:
          dist = np.sqrt(np.square(i.posicionx - k.posicionx) + np.square(i.posiciony - k.posiciony))
          if dist <= i.radio + k.radio:
            i,k = manejo_colision(i,k,cambio_velocidad,n,newt)
  return ldiscos


def sistema_colision_forzada_pares(disc1,disc2,cambio_velocidad,n,newt):
  #Actualización de la posicion para evitar que el sistema fusione los discos
  disc1.posicionx = disc1.arrayposicionx[n-1]
  disc1.posiciony = disc1.arrayposiciony[n-1]
  disc2.posicionx = disc2.arrayposicionx[n-1]
  disc2.posiciony = disc2.arrayposiciony[n-1]
  #Actualizacion de la velocidad
  disc1,disc2 = cambio_velocidad(disc1,disc2)
  return disc1,disc2

def inicializacion_discos(radio, masa, velMin, velMax, grilla, num_discos, random = False, colorRand = False):
  ldiscos = []
  if num_discos <= grilla.subdivisionesx*grilla.subdivisionesy:

    #Creamos una matriz de posiciones para colocar los discos
    matrix_posiciones = np.empty((len(grilla.divisionX)-1,len(grilla.divisionY)-1), dtype=object)
    for i in range(len(grilla.divisionX)-1):
      for j in range(len(grilla.divisionY)-1):
        columnX = grilla.divisionX[i+1] - grilla.dist_entre_separX/2
        filaY = grilla.divisionY[j+1] - grilla.dist_entre_separY/2
        matrix_posiciones[i][j] = [columnX, filaY]

    #inicialización aleatoria con colores iguales (ideal para hacer pruebas estadísticas de una alto numero de discos)
    if random == True and colorRand == False:
      #Se le asigna a cada disco una posicion aleatoria en la matriz de posiciones
      contador = 0
      while contador < num_discos:
          indexX = ri(0,len(grilla.divisionX)-2)
          indexY = ri(0,len(grilla.divisionY)-2)

          if matrix_posiciones[indexY][indexX] != [0,0]:
            posX = matrix_posiciones[indexY][indexX][0]
            posY = matrix_posiciones[indexY][indexX][1]
            veloX = uf(velMin, velMax)
            veloY = uf(velMin, velMax)
            ldiscos.append(Disco(radio, masa, posX, posY ,veloX, veloY))
            contador += 1
            matrix_posiciones[indexY][indexX] = [0,0]
            if contador == num_discos:
              return ldiscos

    #inicialización aleatoria con colores aleatorios
    elif random == True and colorRand == True:
      #Se le asigna a cada disco una posicion aleatoria en la matriz de posiciones
      contador = 0
      while contador < num_discos:
          indexX = ri(0,len(grilla.divisionX)-2)
          indexY = ri(0,len(grilla.divisionY)-2)

          if matrix_posiciones[indexY][indexX] != [0,0]:
            posX = matrix_posiciones[indexY][indexX][0]
            posY = matrix_posiciones[indexY][indexX][1]
            veloX = uf(velMin, velMax)
            veloY = uf(velMin, velMax)
            ldiscos.append(Disco(radio, masa, posX, posY ,veloX, veloY))
            ldiscos[contador].color = ldiscos[contador].colores()
            contador += 1
            matrix_posiciones[indexY][indexX] = [0,0]
            if contador == num_discos:
              return ldiscos

    #inicialización ordenada con colores iguales en los discos
    elif random == False and colorRand == False:
      #Se le asigna a cada disco una posicion en la grilla de manera ordenada, yendo fila por fila llenándolas
      #de abajo hasta arriba
      contador = 0
      for i in range(len(grilla.divisionY)-1):
        for j in range(len(grilla.divisionX)-1):
          posX = matrix_posiciones[j][i][0]
          posY = matrix_posiciones[j][i][1]
          veloX = uf(velMin, velMax)
          veloY = uf(velMin, velMax)
          ldiscos.append(Disco(radio, masa, posX, posY ,veloX, veloY))
          contador += 1
          if contador == num_discos:
            return ldiscos

    #inicialización ordenada con colores aleatorios en los discos
    elif random == False and colorRand == True:
      #Se le asigna a cada disco una posicion en la grilla de manera ordenada, yendo fila por fila llenándolas
      #de abajo hasta arriba
      contador = 0
      for i in range(len(grilla.divisionY)-1):
        for j in range(len(grilla.divisionX)-1):
          posX = matrix_posiciones[j][i][0]
          posY = matrix_posiciones[j][i][1]
          veloX = uf(velMin, velMax)
          veloY = uf(velMin, velMax)
          ldiscos.append(Disco(radio, masa, posX, posY ,veloX, veloY))
          ldiscos[contador].color = ldiscos[contador].colores()
          contador += 1
          if contador == num_discos:
            return ldiscos

  elif num_discos > grilla.subdivisionesx*grilla.subdivisionesy:
    print("El numero de discos es mayor al permitido para el sistema descrito")
    return ldiscos


def graf_discos(discos,caja,fotograma,grilla):
  path = os.getcwd()
  plt.style.use('_mpl-gallery')
  fig, ax = plt.subplots()
  for i in range(len(discos)):
    circ = plt.Circle((discos[i].posicionx, discos[i].posiciony), discos[i].radio,color=discos[i].color)
    ax.add_patch(circ)

  ax.set(xlim=(0, caja.longitudx), xticks=grilla.divisionX,xticklabels="",ylim=(0, caja.longitudy),yticks=grilla.divisionY,yticklabels="")
  plt.savefig(os.path.join(path, f"fotograma{fotograma:04d}.png"))
  plt.close(fig)

def histo_discos(discos,tiempos,tmax,newt):
  path = os.getcwd()
  plt.style.use('_mpl-gallery')

  sizex = tiempos.size
  x = 0.5 + np.arange(sizex)
  contador = 0

  for i in discos:
    y = []
    for j in range(len(i.arrayposiciony)):
      y.append(i.arrayposicionx[j])

    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="blue", linewidth=0.7)

    ax.set(xlim=(0, sizex),
           ylim=(0, 1), yticks=np.arange(0, 1))

    plt.savefig(os.path.join(path, f"histograma{contador:04d}.png"))
    plt.close(fig)
    contador +=1

def crear_video(fps):
  path = os.getcwd()
  filenames = sorted(glob.glob(os.path.join(path, "fotograma*.png")))
  clip = ImageSequenceClip(filenames, fps=fps)
  clip.write_videofile(f"{path}/video_colision.mp4", fps=fps)
  for filename in glob.glob(os.path.join(path, "fotograma*.png")):
     os.remove(filename)
