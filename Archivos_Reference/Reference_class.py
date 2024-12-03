#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf

class Disco:
    def __init__(self, elradio, lamasa, laposicionx,           laposiciony, lavelocidadx, lavelocidady):
        """`__init__(self, elradio, lamasa,                    laposicionx,           laposiciony, lavelocidadx,              lavelocidady)`

        Esta clase se encarga de generar los componentes       necesarios para crear cada disco.

        Examples:
            >>> disco=Disco(1,1,1,1,1,1) #se llama a la clase con esos valores

        Args:
            elradio (float): Un valor que repesenta la medida  del radio de la particula.
            lamasa (int): Un valor que representa la masa de   la particula
            laposicionx (float): Un valor que representa el    componente en el eje x de la posición de la partícula.
            laposiciony (float): Un valor que representa       el        componente en el eje y de la posición de la          partícula.
            lavelocidadx (float): Un valor que representa      el        componente en el eje x de la velocidad de la         partícula.
            lavelocidady (float): Un valor que representa      el        componente en el eje y de la velocidad de la         partícula.
            self.radio (float): Un valor que repesenta la      medida  del radio de la particula.
            lamasa (int): Un valor que representa la masa de   la particula
        """
        self.radio = elradio
        self.masa = lamasa
        self.posicionx = laposicionx
        self.posiciony = laposiciony
        self.velocidadx = lavelocidadx
        self.velocidady = lavelocidady
        self.color = [0,0,1]
        self.arrayposicionx = np.array([self.posicionx])

    def right(self):
        """`right(self)`

        Esta función miembro determina la frontera derecha de  la partícula, para ello hereda los atributos del constructor.

        Examples:
            >>> print(Disco(1,1,1,1,1,1).right())
            2

        Args:
            self.radio (float): Un valor que repesenta la      medida del  radio de la particula.
            slef.posicionx (float): Un valor que representa el componente en el eje x de la posición de la partícula.

        Returns:
            (float): Retorna un valor que representa la        posición de la frontera derecha de la partícula.
        """
        return self.posicionx + self.radio

    #función miembro para obtener el límite izquierdo
    def left(self):
        """ `left(self)`

        Esta función miembro determina la frontera izquierda   de la partícula, para ello hereda los atributos del            constructor.

        Examples:
            >>> Disco(1,1,1,1,1,1).left()
            0

        Args:
            self.radio (float): Un valor que repesenta la      medida del  radio de la particula.
            slef.posicionx (float): Un valor que representa el componente en el eje x de la posición de la partícula.

        Returns:
            (float): Retorna un valor que representa la        posición de la frontera izquierda de la partícula.
        """

        return self.posicionx - self.radio

   #funcion miembro para obtener el límite superior
    def top(self):
        """ `top(self)`

        Esta función miembro determina la frontera superior de la partícula, para ello hereda los atributos del constructor.

        Examples:
            >>> Disco(1,1,1,1,1,1).top()
            2

        Args:
            self.radio (float): Un valor que repesenta la      medida del  radio de la particula.
            slef.posiciony (float): Un valor que representa el componente en el eje y de la posición de la partícula.

        Returns:
            (float): Retorna un valor que representa la        posición de la frontera superior de la partícula.
        """

        return self.posiciony + self.radio

   #funcion miembro para obtener el límite inferior
    def bottom(self):
        """`bottom(self)`

        Esta función miembro determina la frontera inferior de la partícula, para ello hereda los atributos del               constructor.

        Examples:
            >>> Disco(1,1,1,1,1,1).bottom()
            0

        Args:
            self.radio (float): Un valor que repesenta la      medida del  radio de la particula.
            slef.posiciony (float): Un valor que representa el componente en el eje y de la posición de la partícula.

        Returns:
            (float): Retorna un valor que representa la        posición de la frontera inferior de la partícula.
        """

        return self.posiciony - self.radio

class Box:
    def __init__(self,lalongitudX,lalongitudY):
        """`__init__(self,lalongitudX,lalongitudY)`

        Esta clase se encarga de generar una caja donde se     colocará la grilla.

        Examples:
            >>> caja=Box(1,1) #Se llama a la clase con estos valores

        Args:
            lalongitudX (int): Un valor que repesenta el largo de la caja.
            lalongitudy (int): Un valor que repesenta el ancho de la caja.
        """
        self.longitudx = lalongitudX
        self.longitudy = lalongitudY



class Grilla:
    def __init__(self,xmax,ymax,ldiscos):
        """`__init__(self,xmax,ymax,ldiscos)`

        Esta clase se encarga de generar una grilla donde      colocar a las partículas.

        Examples:
            >>> girlla=Grilla(10,10,1) #Se llama a la clase con estos valores

        Args:
            xmax (int): Un valor que repesenta el valor maximo de x.
            ymax (int): Un valor que repesenta el ancho maximo de y.
            ldiscos (list): Es una lista donde cada elemento   que la compone es un disco con las caracteristicas propias del mismo.
        """

        self.xmax = xmax
        self.subdivisionesx = int(xmax/(2*ldiscos[0].radio))   #cantidad de subdivisiones en el eje x
        self.subdivisionesy = int(ymax/(2*ldiscos[0].radio))   #cantidad de subdivisiones en el eje y


        def creacion_grilla(self,xmax,ldiscos):
            """Esta función dentro del constructor crea un     arreglo con todos los valores de x y de y.

            Args:
                xmax (int): Un valor que repesenta el valor    maximo de x.
                ymax (int): Un valor que repesenta el ancho    maximo de y.
                ldiscos (list): Es una lista donde cada        elemento que la compone es un disco con las caracteristicas    propias del     mismo.

            """
            divisionX = np.linspace(0,xmax,self.subdivisionesx)
            dist_entre_separX = divisionX[1]
            return divisionX, dist_entre_separX

        self.divisionX = creacion_grilla(self,xmax,ldiscos)[0]
        self.divisionY = creacion_grilla(self,ymax,ldiscos)[0]
        self.dist_entre_separX = creacion_grilla(self,xmax,    ldiscos)[1]



