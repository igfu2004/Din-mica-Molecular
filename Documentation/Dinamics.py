#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf

class Disco:
    def __init__(self, elradio, lamasa, laposicionx, laposiciony, lavelocidadx, lavelocidady):
        """`__init__(self, elradio, lamasa, laposicionx,           laposiciony, lavelocidadx, lavelocidady)`

        Esta clase se encarga de generar los componentes necesarios para crear cada disco.

        Args:
            elradio (float): Un valor que repesenta la medida del radio de la particula.
            lamasa (int): Un valor que representa la masa de la particula
            laposicionx (float): Un valor que representa el componente en el eje x de la posición de la partícula.
            laposiciony (float): Un valor que representa el        componente en el eje y de la posición de la partícula.
            lavelocidadx (float): Un valor que representa el        componente en el eje x de la velocidad de la partícula.
            lavelocidady (float): Un valor que representa el        componente en el eje y de la velocidad de la partícula.
            self.radio (float): Un valor que repesenta la medida  del radio de la particula.
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

        Esta función miembro determina la frontera derecha de la partícula, para ello hereda los atributos del constructor.

        Examples:
            >>> Disco(1,1,1,1,1,1).right()
            2

        Args:
            self.radio (float): Un valor que repesenta la medida del  radio de la particula.
            slef.posicionx (float): Un valor que representa el componente en el eje x de la posición de la partícula.

        Returns:
            (float): Retorna un valor que representa la posición de la frontera derecha de la partícula.
        """
        return self.posicionx + self.radio

    #función miembro para obtener el límite izquierdo
    def left(self):
        """ left(self)`

        Esta función miembro determina la frontera izquierda de la partícula, para ello hereda los atributos del constructor.

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

        Esta función miembro determina la frontera inferior de la partícula, para ello hereda los atributos del            constructor.

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

        Esta clase se encarga de generar una caja donde se colocará la grilla.

        Args:
            lalongitudX (int): Un valor que repesenta el largo de la caja.
            lalongitudy (int): Un valor que repesenta el ancho de la caja.
        """
        self.longitudx = lalongitudX
        self.longitudy = lalongitudY



class Grilla:
    def __init__(self,xmax,ymax,ldiscos):
        """`__init__(self,xmax,ymax,ldiscos)`

        Esta clase se encarga de generar una grilla donde colocar a las partículas.

        Args:
            xmax (int): Un valor que repesenta el valor maximo de x.
            ymax (int): Un valor que repesenta el ancho maximo de y.
            ldiscos (list): Es una lista donde cada elemento que la compone es un disco con las caracteristicas propias del mismo.
        """

        self.xmax = xmax
        self.subdivisionesx = int(xmax/(2*ldiscos[0].radio)) #cantidad de subdivisiones en el eje x
        self.subdivisionesy = int(ymax/(2*ldiscos[0].radio)) #cantidad de subdivisiones en el eje y

        def creacion_grilla(self,xmax,ldiscos):
            """Esta función dentro del constructor crea un arreglo con todos los valores de x y de y.

            Args:
                xmax (int): Un valor que repesenta el valor maximo de x.
                ymax (int): Un valor que repesenta el ancho maximo de y.
                ldiscos (list): Es una lista donde cada elemento que la compone es un disco con las caracteristicas propias del     mismo.

            """
            divisionX = np.linspace(0,xmax,self.subdivisionesx)
            dist_entre_separX = divisionX[1]
            return divisionX, dist_entre_separX

        self.divisionX = creacion_grilla(self,xmax,ldiscos)[0]
        self.divisionY = creacion_grilla(self,ymax,ldiscos)[0]
        self.dist_entre_separX = creacion_grilla(self,xmax,ldiscos)[1]


def nueva_posicion(disco, dt):
    """`nueva_posicion(disco, dt)`

    Esta función se encarga de ubicar la nueva posición de cada disco en la grilla.

    Args:
         disco (Disco): Son todas las caracteristicas de los discos inicializadas en la clase Disco.
         dt (float): Toma un elemento que representa el tiempo, es decir, el momento cuando se esta realizando el movimiento.

    Returns:
        disco (Disco): Retorna las caracteristicas del disco actualizadas.
    """
    disco.posicionx += disco.velocidadx * dt
    disco.posiciony += disco.velocidady * dt
    disco.arrayposicionx = np.append(disco.arrayposicionx,disco.posicionx)
    disco.arrayposiciony = np.append(disco.arrayposiciony,disco.posiciony)
    return disco


def deteccion_colision_pared(disco,lx,ly,n,newt):
    """`deteccion_colision_pared(disco,lx,ly,n,newt)`

    Esta función se encarga de detectar si se esta llevando a cabo una colisión con alguna pared, para ello determina el valor del tiempo en el siguiente       fotograma, y compara la posición del disco con la de la pared para determinar   si colisionaran o no.

    Args:
        disco (Disco): Son todas las caracteristicas de los   discos            inicializadas en la clase Disco.
        lx (int): Toma el valor del largo de la caja.
        ly (int): Toma el valor del ancho de la caja.
        n (int): Representa el valor del momento actual.
        newt (float): Representa 1 dividido entre la cantidad de FPS.

    Returns:
        disco (Disco): Retorna las caracteristicas del disco actualizadas.
    """
    #Calculamos el tiempo hasta el próximo fotograma
    tprox = (n+1)*newt
  #Esta parte viene de realizar una parametrización de la trayectoria del disco por medio de la ecuación paramétrica de la recta.
  #Buscamos el tiempo t entre el intervalo de [0,1] en el que se causa la colisión con la pared
    posicioninicial = disco.right()
    posicionfinal = disco.right() + disco.velocidadx*tprox
    if posicionfinal >= lx:
        t = (lx - disco.right())/(posicionfinal - disco.right())
        x = disco.right() + t*(posicionfinal-disco.right())
        disco.posicionx = x - disco.radio
        disco.velocidadx *= -1

    posicioninicial = disco.left()
    posicionfinal = disco.left() + disco.velocidadx*tprox
    if posicionfinal <= 0:
        t = -1*disco.left()/(posicionfinal - disco.left())
        x = disco.left() + t*(posicionfinal-disco.left())
        disco.posicionx = x + disco.radio
        disco.velocidadx *= -1

    posicioninicial = disco.top()
    posicionfinal = disco.top() + disco.velocidady*tprox
    if posicionfinal >= ly:
        t = (ly - disco.top())/(posicionfinal - disco.top())
        y = disco.top() + t*(posicionfinal-disco.top())
        disco.posiciony = y - disco.radio
        disco.velocidady *= -1

    posicioninicial = disco.bottom()
    posicionfinal = posicioninicial + disco.velocidady*tprox
    if posicionfinal <= 0:
        t = -1*disco.bottom()/(posicionfinal - disco.bottom())
        y = disco.bottom() + t*(posicionfinal - disco.bottom())
        disco.posiciony = y + disco.radio
        disco.velocidady *= -1

    return disco



def acomodo_inicial_discos(radio, masa, velMin, velMax, caja, num_discos):
    """`acomodo_inicial_discos(radio, masa, velMin, velMax,        caja, num_discos)`

    Esta función se encarga de generar el acomodo inicial de las partículas en la grilla.

    Args:
        radio (float): El radio de la partícula.
        masa (int): La masa de la partícula.
        velMin (float): El valor mínimo de la velocidad de la partícula.
        velMax (float): El valor máximo de la velocidad de la partícula.
        caja (Box): Son los componentes de la caja que contiene la grilla.
        num_discos (int): La cantidad de partículas.

    Returns:
        ldiscos (list): Retorna una lista con los datos de todos los discos.
    """
    ldiscos = []
    if num_discos == 1:
        posX = caja.longitudx/2
        posY = caja.longitudy/2
        veloX = uf(velMin, velMax)
        veloY = uf(velMin, velMax)
        ldiscos.append(Disco(radio, masa, posX, posY ,veloX, veloY))

    elif num_discos <= 0:
        print("El numero de discos debe ser mayor a 0.")

    else:
        if type(num_discos) == int:
            if (num_discos/2)%(2) == 0:
                num_subdivisionx = int(num_discos/2)
                num_subdivisiony = num_subdivisionx
                posiciones_x = np.linspace(0.02+radio,caja.longitudx-radio-0.02,num_subdivisionx)
                posiciones_y = np.linspace(0.02+radio,caja.longitudy-radio-0.02,num_subdivisiony)
            else:
                num_subdivisionx = int((num_discos+1)/2)
                num_subdivisiony = int((num_discos-1)/2)
                posiciones_x = np.linspace(radio,caja.longitudx-radio,num_subdivisionx)
                posiciones_y = np.linspace(radio,caja.longitudy-radio,num_subdivisiony)
            for i in range(num_subdivisionx):
                for j in range(num_subdivisiony):
                    posX = posiciones_x[i]
                    posY = posiciones_y[j]
                    veloX = uf(velMin, velMax)
                    veloY = uf(velMin, velMax)
                    ldiscos.append(Disco(radio, masa, posiciones_x[i], posiciones_y[j] ,veloX, veloY))


        else:
            print("El numero de discos debe ser un entero")
    return ldiscos

def graf_discos(discos,caja,fotograma,grilla):
    """`graf_discos(discos,caja,fotograma,grilla)`

    Esta función se encarga de graficar cada frame.

    Args:
        discos (Disco): Son todas las caracteristicas de los discos inicializadas en la clase Disco.
        caja (Box): Contiene las caracteristicas de la caja que almacena la grilla.
        fotograma (int): (No se uso en la función revisar en versiones posteriores si se elimina).
        grilla (Grilla): Contiene la información de la grilla.
    """
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    colors = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1]]
    #colors = np.random.uniform(15, 80, len(discos))
    for i in range(len(discos)):
        r = np.round(np.random.rand(),1)
        g = np.round(np.random.rand(),1)
        b = np.round(np.random.rand(),1)
        circ = plt.Circle((discos[i].posicionx, discos[i].posiciony), discos[i].radio,color=colors[i])
        #ax.scatter(discos[i].posicionx, discos[i].posiciony,s=discos[i].radio, color=colors[i])
        ax.add_patch(circ)
    ax.set(xlim=(0, caja.longitudx), xticks=grilla.divisionX,xticklabels="",ylim=(0, caja.longitudy),yticks=grilla.divisionY,yticklabels="")
  #falta guardarlo en una carpeta, por el momento solo es para ver si se grafica bien
    plt.show()
    plt.close()

def histo_discos(discos,tiempos,tmax,newt):
    """`histo_discos(discos,tiempos,tmax,newt)`

    Esta función crea un histograma de las posiciones de los centros a lo largo del eje x.

    Args:
        discos (Disco): Son todas las caracteristicas de los discos    inicializadas en la clase Disco.
        tiempos (array): Un array que contiene los valores de tiempo.
        tmax (int): Representa el valor máximo del tiempo.
        newt (float): Representa 1 dividido entre la cantidad de FPS.

    """
    plt.style.use('_mpl-gallery')
    sizex = tiempos.size
    x = 0.5 + np.arange(sizex)

    for i in discos:
        y = []
        for j in range(len(i.arrayposiciony)):
            y.append(i.arrayposicionx[j])

        # plot
        fig, ax = plt.subplots()

        ax.bar(x, y, width=1, edgecolor="blue", linewidth=0.7)

        ax.set(xlim=(0, sizex),
               ylim=(0, 1), yticks=np.arange(0, 1))

        plt.show()
def cambio_velocidad_colision_pares(disco1,disco2):
    """`cambio_velocidad_colision_pares(disco1,disco2)`

    Esta función se encarga de determinar la nueva velocidad de los discos después de que colisionan.

    Args:
        disco1 (Disco): Toma las caracterísiticas de uno de los discos que esta colisionando.
        disco2 (Disco): Toma las caracterísiticas de uno de los discos que      esta colisionando.

    Returns:
        disco1 (Disco): Retorna las caracteristicas de este disco actualizadas.
        disco2 (Disco): Retorna las caracteristicas de este disco               actualizadas.
   """
    v1x = (disco1.velocidadx*(disco1.masa - disco2.masa) + 2*disco2.masa*disco2.velocidadx)/(disco1.masa + disco2.masa)
    v1y = (disco1.velocidady*(disco1.masa - disco2.masa) + 2*disco2.masa*disco2.velocidady)/(disco1.masa + disco2.masa)
    v2x = (disco2.velocidadx*(disco2.masa - disco1.masa) + 2*disco1.masa*disco1.velocidadx)/(disco1.masa + disco2.masa)
    v2y = (disco2.velocidady*(disco2.masa - disco1.masa) + 2*disco1.masa*disco1.velocidady)/(disco1.masa + disco2.masa)

    disco1.velocidadx = v1x
    disco1.velocidady = v1y
    disco2.velocidadx = v2x
    disco2.velocidady = v2y

    return disco1, disco2


def deteccion_colision_pares(grilla,ldiscos,cambio_velocidad,n,newt,manejo_colision):
    """ `deteccion_colision_pares(grilla,ldiscos,cambio_velocidad,n,newt,            manejo_colision)`

    Esta función se encarga de la verificación de posiciones en un grilla y en sus vecinas inmediatas        sobre el eje x para determinar si se esta llevando a cabo una colisión entre partículas.

    Args:
        grilla (Grilla): Contiene la información de la grilla.
        ldiscos (list): Una lista que contiene la información de los discos.
        cambio_velocidad (function): Llama a una función para determinar el cambio de velocidades causado por la colisión.
        n (int): representa el valor del momento actual.
        newt (float): Representa 1 dividido entre la cantidad de FPS.
        manejo_colision (function): Llama a una función para el manejo de la colisión.

    Returns:
        ldiscos (list): Una lista que contiene la información actulizada de los discos.
    """

    #verificación de posiciones en un grilla y en sus vecinas inmediatas sobre el eje x
    for j in grilla.divisionX:
        discos_en_grilla = []
        for i in range(len(ldiscos)):
            if abs(ldiscos[i].posicionx - j) < (2*grilla.dist_entre_separX):
                discos_en_grilla.append(ldiscos[i])

    #descartamos los discos que no se sobreponen en X
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
    """`sistema_colision_forzada_pares(disc1,disc2,cambio_velocidad,n,newt)`

    Esta función se encarga de actualizar la posición de las partículas para evitar que los discos se fucionen.

    Args:
        disco1 (Disco): Toma las caracterísiticas de uno de los discos que esta colisionando.
        disco2 (Disco): Toma las caracterísiticas de uno de los discos que      esta colisionando.
        cambio_velocidad (function): Llama a una función para determinar el     cambio de velocidades causado por la colisión.
        n (int): representa el valor del momento actual.
        newt (float): Representa 1 dividido entre la cantidad de FPS.
        manejo_colision (function): Llama a una función para el manejo de la    colisión.

    Returns:
        disco1 (Disco): Retorna las caracteristicas de este disco actualizadas.
        disco2 (Disco): Retorna las caracteristicas de este disco               actualizadas.
    """
    #Actualización de la posicion para evitar que el sistema fusione los discos
    disc1.posicionx = disc1.arrayposicionx[n-1]
    disc1.posiciony = disc1.arrayposiciony[n-1]
    disc2.posicionx = disc2.arrayposicionx[n-1]
    disc2.posiciony = disc2.arrayposiciony[n-1]
  #Actualización de la velocidad
    disc1,disc2 = cambio_velocidad(disc1,disc2)
    return disc1,disc2
