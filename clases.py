#!/usr/bin/env python3
import numpy as np
from random import randint as ri

class Disco:
    """
    Representa un disco en el sistema que trabajaremos.

    Attributes:
    radio (float): el radio del disco
    masa (float): la masa del disco
    posicionx (float): la posición del disco en el eje X
    posiciony (float): la posición del disco en el eje Y
    velocidadx (float): la velocidad en el eje X
    velocidady (float): la velocidad en el eje Y
    color (list): el color del disco
    """
    def __init__(self, elradio, lamasa, laposicionx, laposiciony, lavelocidadx, lavelocidady):
        """
        Inicializa un disco con sus propiedades físicas.

        Args:
            elradio (float): radio del disco
            lamasa (float): masa del disco
            laposicionx (float): posicion inicial en el eje X
            laposiciony (float): posicion inicial en el eje Y
            lavelocidadx (float): velocidad inicial del disco en eje X
            lavelocidady (float): velocidad inicial del disco en eje Y
        """
        self.radio = elradio
        self.masa = lamasa
        self.posicionx = laposicionx
        self.posiciony = laposiciony
        self.velocidad = np.array([lavelocidadx,lavelocidady])
        self.color = [0,0,1]
        #posicion de los discos para crear el histograma
        self.arrayposicionx = np.array([])
        self.arrayposiciony = np.array([])
    
    #Variacion de las fronteras
    #función miembro para obtener el límite derecho
    def right(self):
        return self.posicionx + self.radio

    #función miembro para obtener el límite izquierdo
    def left(self):
        return self.posicionx - self.radio

    #funcion miembro para obtener el límite superior
    def top(self):
        return self.posiciony + self.radio

    #funcion miembro para obtener el límite inferior
    def bottom(self):
        return self.posiciony - self.radio
    
    #funcion para cambiar el color del disco de manera aleatoria
    def colores(self):
      colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[0,0,0]]
      new_color_number = ri(0,len(colors)-1)
      new_color = colors[new_color_number]
      return new_color

class Box:
    def __init__(self,lalongitudX,lalongitudY):
      self.longitudx = lalongitudX
      self.longitudy = lalongitudY

class Grilla:
  def __init__(self,xmax,ymax,radio):
    self.xmax = xmax
    self.ymax = ymax
    self.subdivisionesx = int(xmax/(2*radio)) #Cantidad de subdivisiones en el eje x
    self.subdivisionesy = int(ymax/(2*radio)) #Cantidad de subdivisiones en el eje y

    def creacion_grilla(self,xmax,ldiscos):
      divisionX = np.linspace(0,xmax,self.subdivisionesx)
      divisionY = np.linspace(0,ymax,self.subdivisionesy)
      dist_entre_separX = divisionX[1]
      dist_entre_separY = divisionY[1]
      return divisionX, divisionY, dist_entre_separX, dist_entre_separY

    self.divisionX, self.divisionY, self.dist_entre_separX, self.dist_entre_separY = creacion_grilla(self,xmax,ymax)
