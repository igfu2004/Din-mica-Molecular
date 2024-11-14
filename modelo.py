#!/usr/bin/env python3
import numpy as np

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


class Box:
    def __init__(self,lalongitudX,lalongitudY):
      self.longitudx = lalongitudX
      self.longitudy = lalongitudY

class Grilla:
  def __init__(self,xmax,ymax,ldiscos):
    self.xmax = xmax
    self.subdivisionesx = int(xmax/(2*ldiscos[0].radio))
    self.subdivisionesy = int(ymax/(2*ldiscos[0].radio))

    def creacion_grilla(self,xmax,ldiscos):
      divisionX = np.linspace(0,xmax,self.subdivisionesx)
      divisionY = np.linspace(0,ymax,self.subdivisionesy)
      dist_entre_separX = divisionX[1]
      return divisionX, dist_entre_separX
    self.divisionX = creacion_grilla(self,xmax,ldiscos)[0]
    self.divisionY = creacion_grilla(self,ymax,ldiscos)[0]
    self.dist_entre_separX = creacion_grilla(self,xmax,ldiscos)[1]










