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
    """`nueva_posicion(disco, dt)`

    Esta función se encarga de ubicar la nueva posición de cada disco en la grilla. con base en la ecuación $x_f = x_0 + vt$.

    Examples:
        >>> posicion=nueva_posicion(Disco(1,1,1,1,1,1),1) # A esta variable se le asigna una nueva posición apartir de los datos del disco y el cambio del tiempo


    Args:
         disco (Disco): Son todas las caracteristicas de los discos inicializadas en la clase Disco.
         dt (float): Toma un elemento que representa el tiempo, es decir, el momento cuando se esta realizando el movimiento.

    Returns:
        disco (Disco): Retorna las caracteristicas del disco actualizadas.
    """
    #funcion para una nueva posicion del disco al moverse
    #con la ec. x_f = x_0 + vt
    posxFinal = disco.posicionx + disco.velocidad[0] * dt
    posyFinal = disco.posiciony + disco.velocidad[1] * dt

    disco.posicionx = posxFinal
    disco.posiciony = posyFinal

    disco.arrayposicionx = np.append(disco.arrayposicionx,posxFinal)
    disco.arrayposiciony = np.append(disco.arrayposiciony,posyFinal)
    return disco


def tiempo_colision_pared(disco,lx,ly,newt):
    #Esta parte viene de realizar una parametrización de la trayectoria del disco por medio de la ecuación paramétrica de la recta.
    #Buscamos el tiempo t entre el intervalo de [0,1] en el que se causa la colisión con la pared
    """
    `tiempo_colision_pared(disco,lx,ly,newt)`

    Esta función se encarga de realizar una parametrización de la trayectoria del disco por medio de la ecuación paramétrica de la    recta. Con el objetivo de buscar un tiempo t entre el intervalo de [0,1] en el que se causa la colisión con la pared.

    Examples:
        >>> print(tiempo_colision_pared(Disco(1,1,1,0,2,1),0.5,1,1))
        1.0

    Args:
         disco (Disco): Son todas las caracteristicas de los discos inicializadas en la clase Disco.
         lx (float): Representa la longitud en el eje x de la caja.
         ly (float): Representa la longitud en el eje y de la caja.
         newt (float): Representa 1 dividido entre la cantidad de FPS.


    Returns:
        t (float): Retorna un float que representa el momento donde se da la closión.

    """
    t = 10000000000

    posicioninicial = disco.right()
    posicionfinal = disco.right() + disco.velocidad[0]*newt
    if posicionfinal >= lx:
        t = (lx - disco.right())/(posicionfinal - disco.right())

    posicioninicial = disco.left()
    posicionfinal = disco.left() + disco.velocidad[0]*newt
    if posicionfinal <= 0:
        t = -1*disco.left()/(posicionfinal - disco.left())

    posicioninicial = disco.top()
    posicionfinal = disco.top() + disco.velocidad[1]*newt
    if posicionfinal >= ly:
        t = (ly - disco.top())/(posicionfinal - disco.top())

    posicioninicial = disco.bottom()
    posicionfinal = posicioninicial + disco.velocidad[1]*newt
    if posicionfinal <= 0:
        t = -1*disco.bottom()/(posicionfinal - disco.bottom())

    return t


def deteccion_colision_pared_con_manejo(disco,lx,ly,newt):
    """`deteccion_colision_pared_con_manejo(disco,lx,ly,newt)`

    Esta función se encarga de utilizar la ecuación de la recta parametrizada para realizar la colisión como si se tratara de una colisión unidimensional.

    Examples:
       >>>  colision=deteccion_colision_pared_con_manejo(Disco(1,1,1,1,1,1),1,1,1) #Se llama a la funcion para actulizar los datos del disco

    Args:
        disco (Disco): Son todas las caracteristicas de los   discos            inicializadas en la clase Disco.
        lx (int): Toma el valor del largo de la caja.
        ly (int): Toma el valor del ancho de la caja.
        newt (float): Representa 1 dividido entre la cantidad de FPS.

    Returns:
        disco (Disco): Retorna las caracteristicas del disco actualizadas.
    """
    #Esta parte viene de realizar una parametrización de la trayectoria del disco por medio de la ecuación paramétrica de la recta.
  #Buscamos el tiempo t entre el intervalo de [0,1] en el que se causa la colisión con la pared
    posicioninicial = disco.right()
    posicionfinal = disco.right() + disco.velocidad[0]*newt
    if posicionfinal >= lx:
        t = (lx - disco.right())/(posicionfinal - disco.right())
        x = disco.right() + t*(posicionfinal-disco.right())
        disco.posicionx = x - disco.radio
        disco.velocidadx[0] *= -1

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

def cambio_velocidad_colision_pares(disco1, disco2):
    """`cambio_velocidad_colision_pares(disco1, disco2)`

    Esta función se encarga por medio del analisis de los vectores de las partículas y las ecuaciones de colisiones elásticas de determinar el cambio de velocidades cuando se dan colisiones entre dos de estas.

    Examples:
        >>> cambio= cambio_velocidad_colision_pares(Disco(1,1,1,1,1,1),Disco(2,2,2,2,2,2)) #Se le asigna a la variable el cambio de velocidad de las partículas después de la colisión


    Args:
        disco1 (Disco): Contiene todas las características de una de las partículas.
        disco2 (Disco): Contiene todas las características de una de las partículas.


    Returns:
        disco1 (Disco): Contiene todas las características de una de las partículas actualizadas después de la colisión.
        disco2 (Disco): Contiene todas las características de una de las partículas actualizadas después de la colisión.


    """
    # Añadir un margen de tolerancia para evitar problemas de sobreposición
    MARGEN_TOLERANCIA = 1e-5  # ajustar este valor según lo que se necesite


    # Buscamos el vector entre el centro de los discos
    n = np.array([disco2.posicionx - disco1.posicionx, disco2.posiciony - disco1.posiciony])

    # Calculamos la distancia entre los discos
    dist = np.linalg.norm(n)

    # Si la distancia entre los discos es muy pequeña (por ejemplo, están sobrepuestos o casi),
    # agregamos un pequeño desplazamiento para separarlos.
    if dist < disco1.radio + disco2.radio + MARGEN_TOLERANCIA:
        # Separamos los discos ligeramente para evitar que se queden bloqueados
        separacion = disco1.radio + disco2.radio - dist + MARGEN_TOLERANCIA
        n = n / dist if dist != 0 else np.zeros_like(n)  # Normalizamos el vector n
        disco1.posicionx -= 0.5 * separacion * n[0]
        disco1.posiciony -= 0.5 * separacion * n[1]
        disco2.posicionx += 0.5 * separacion * n[0]
        disco2.posiciony += 0.5 * separacion * n[1]

    # Normalizamos el vector de colisión
    if np.linalg.norm(n) == 0:
        nu = np.zeros_like(n)
    else:
        nu = n / np.linalg.norm(n)

    # Buscamos el vector tangente unitario a los discos (perpendicular al vector normal)
    vect = np.array([-1 * nu[1], nu[0]])

    # Componente normal y tangencial de las velocidades de los discos
    v1n = np.dot(disco1.velocidad, nu)
    v2n = np.dot(disco2.velocidad, nu)
    v1t = np.dot(disco1.velocidad, vect)
    v2t = np.dot(disco2.velocidad, vect)

    # Fórmulas de colisión elástica para las velocidades normales
    v1nfinal = (v1n * (disco1.masa - disco2.masa) + 2 * disco2.masa * v2n) / (disco1.masa + disco2.masa)
    v2nfinal = (v2n * (disco2.masa - disco1.masa) + 2 * disco1.masa * v1n) / (disco1.masa + disco2.masa)

    # Componentes de las velocidades finales en las direcciones normal y tangencial
    v1nPrima = v1nfinal * nu
    v2nPrima = v2nfinal * nu
    v1tPrima = v1t * vect
    v2tPrima = v2t * vect

    # Velocidades finales de los discos (en el sistema de coordenadas cartesiano)
    v1Prima = v1nPrima + v1tPrima
    v2Prima = v2nPrima + v2tPrima

    # Actualizamos las velocidades de los discos
    disco1.velocidad[0] = v1Prima[0]
    disco1.velocidad[1] = v1Prima[1]
    disco2.velocidad[0] = v2Prima[0]
    disco2.velocidad[1] = v2Prima[1]

    return disco1, disco2


def colision_proxima(grilla,ldiscos,cambio_velocidad,newt,manejo_colision,det_pared,manejo_pared,lx,ly):
    """
    `colision_proxima(grilla),ldiscos,cambio_velocidad,newt,manejo_colision,det_pared,manejo_pared,lx,ly)`

    Esta función se encarga de determinar cual será la colisión más proxima a ocurrir.

    Examples:
        >>> discos = colision_proxima(Grilla(10,10,1),[Disco(1,1,1,1,1,1),Disco(2,2,2,2,2,2)],cambio_velocidad_colision_pares,1/60,manejo_de_colisiones_pares,tiempo_colision_pared,deteccion_colision_pared_con_manejo,caja.longitudx,caja.longitudy) #Utilizando las funciones y clases anteriores se puede implementar esta función para verificar que colision se esta dando primero


    Args:
        grilla (Grilla): una variable que almacena los datos de la grilla.
        ldiscos (list): Una lista que contiene los datos de todos los discos en la grilla.
        cambio_velocidad (funcion): Una función para determinar el cambio de velocidad debido a las colisiones.
        newt (float): Un valor que representa el lapso de tiempo hasta el siguiente fotograma.
        manejo_colision (funcion): Una función que permita el manejo de la colisión.
        det_pared (funcion): Una función para determinar la colisión con la pared.
        majeno_pared (funcion): Una funcion que se encarga del manejo de la colisión con pared.
        lx (float) : La longitud de la caja que contiene la grilla.
        ly (float): El ancho de la caja que contiene la grilla.


    Returns:
        ldiscos (list): Retorna la lista que contiene la información de los discos con dicha información actualizada.
    """
    #verificación de posiciones en un grilla y en sus vecinas inmediatas sobre el eje x
    for j in grilla.divisionX:
        discos_en_grilla = []
        for i in range(len(ldiscos)):
            if abs(ldiscos[i].posicionx - j) < (2*grilla.dist_entre_separX):
                discos_en_grilla.append(ldiscos[i])

        #descartamos los discos que no se sobreponen en X
        posb_colisiones = []
        for i in discos_en_grilla:
            for k in discos_en_grilla:
                if i == k:
                    pass
                else:
                    #Buscamos el tiempo hasta la siguiente colision
                    #Vemos cual es la siguiente posicion de los discos, para saber si hay colision en el siguiente fotograma
                    new_pos_ix = i.posicionx + i.velocidad[0]*newt
                    new_pos_kx = k.posicionx + k.velocidad[0]*newt
                    new_pos_iy = i.posiciony + i.velocidad[1]*newt
                    new_pos_ky = k.posiciony + k.velocidad[1]*newt
                    dist_centros_final = np.sqrt(np.square(new_pos_ix - new_pos_kx) + np.square(new_pos_iy - new_pos_ky))
                    if dist_centros_final <= i.radio + k.radio:
                        dist_centros = np.sqrt(np.square(i.posicionx - k.posicionx) + np.square(i.posiciony - k.posiciony))
                        dist_fronteras = dist_centros - i.radio - k.radio

                        #Buscamos el tiempo hasta la colision
                        time_colision_pares = dist_fronteras/(np.linalg.norm(i.velocidad)+np.linalg.norm(k.velocidad))

                        #Buscamos el tiempo hasta la colision con una pared en ambos discos
                        time_col_wall_i = det_pared(i,lx,ly,newt)
                        time_col_wall_k = det_pared(k,lx,ly,newt)

                        if time_colision_pares < time_col_wall_i or time_colision_pares < time_col_wall_k:
                            i,k = manejo_colision(i,k,cambio_velocidad,newt)

                        elif time_colision_pares > time_col_wall_i and time_colision_pares > time_col_wall_k:
                            i = manejo_pared(i,lx,ly,newt)
                            k = manejo_pared(k,lx,ly,newt)

                        elif time_colision_pares == time_col_wall_i or time_colision_pares == time_col_wall_k:
                            i,k = manejo_colision(i,k,cambio_velocidad,newt)
                            i = manejo_pared(i,lx,ly,newt)
                            k = manejo_pared(k,lx,ly,newt)
                i = manejo_pared(i,lx,ly,newt)

    return ldiscos

def manejo_de_colisiones_pares(disc1,disc2,cambio_velocidad,newt):
    """`manejo_de_colisiones_pares(disc1,disc2,cambio_velocidad,newt) `

    Esta función realiza ajustes en la posición de las partículas después de colisionar entre ellas para asegurar que no se sobrepongan con partículas cercanas.

    Examples:
        >>> cambio= manejo_de_colisiones_pares(Disco(1,1,1,1,1,1),Disco(2,2,2,2,2,2),cambio_velocidad_colision_pares,1) #Se le asigna a la variable el cambio de velocidad de las partículas después de la colisión


    Args:
        disco1 (Disco): Contiene todas las características de una de las partículas.
        disco2 (Disco): Contiene todas las características de una de las partículas.
        cambio_velocidad (funcion): Una funcion que determine el cambio de la velocidad.
        newt (float): Un valor que representa el paso del tiempo.
    """
    #Cambiamos las velocidades de los debido a la colision
    disc1,disc2 = cambio_velocidad(disc1,disc2)
    #Hacemos una subrutina de paso temporal en dt extremadamente pequeños hasta que los discos dejen
    #de colisionar entre si con las nuevas velocidades
    dt = newt/100
    distancia = np.sqrt(np.square(disc1.posicionx - disc2.posicionx) + np.square(disc1.posiciony - disc2.posiciony))
    posx1 = disc1.posicionx
    posy1 = disc1.posiciony
    posx2 = disc2.posicionx
    posy2 = disc2.posiciony
    while distancia <= disc1.radio + disc2.radio:
        posx1 += disc1.velocidad[0] * dt
        posy1 += disc1.velocidad[1] * dt
        posx2 += disc2.velocidad[0] * dt
        posy2 += disc2.velocidad[1] * dt
        distancia = np.sqrt(np.square(posx1 - posx2) + np.square(posy1 - posy2))

    disc1.posicionx = posx1
    disc1.posiciony = posy1
    disc2.posicionx = posx2
    disc2.posiciony = posy2

    return disc1,disc2


def inicializacion_discos(radio, masa, velMin, velMax, grilla, num_discos, random = False, colorRand = False):
    """`inicializacion_discos(radio, masa, velMin, velMax, grilla, num_discos, random = False, colorRand = False)`

    Esta función se encarga de generar el acomodo inicial de las partículas en la grilla.

    Args:
        radio (float): El radio de la partícula.
        masa (int): La masa de la partícula.
        velMin (float): El valor mínimo de la velocidad de la partícula.
        velMax (float): El valor máximo de la velocidad de la partícula.
        grilla (Grilla): Son los componentes de la grilla.
        num_discos (int): La cantidad de partículas.
        random (boolean): Implica si se desea un acomodo inicial aleatorio o no.
        color (boolean): Implica si se quiere que las partículas tengan diferentes colores o no.

    Returns:
        ldiscos (list): Retorna una lista con los datos de todos los discos.
    """

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
    """`graf_discos(discos,caja,fotograma,grilla)`

    Esta función se encarga de graficar cada frame.

    Args:
        discos (Disco): Son todas las caracteristicas de los discos inicializadas en la clase Disco.
        caja (Box): Contiene las caracteristicas de la caja que almacena la grilla.
        fotograma (int): (No se uso en la función revisar en versiones posteriores si se elimina).
        grilla (Grilla): Contiene la información de la grilla.

    Returns:
        disco1 (Disco): Contiene todas las características de una de las partículas actualizadas después de la colisión.
        disco2 (Disco): Contiene todas las características de una de las partículas actualizadas después de la colisión.
    """
    path = os.getcwd()
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    for i in range(len(discos)):
        circ = plt.Circle((discos[i].posicionx, discos[i].posiciony), discos[i].radio,color=discos[i].color)
        ax.add_patch(circ)

    ax.set(xlim=(0, caja.longitudx), xticks=grilla.divisionX,xticklabels="",ylim=(0, caja.longitudy),yticks=grilla.divisionY,yticklabels="")
    plt.savefig(os.path.join(path, f"fotograma{fotograma:04d}.png"))
    plt.close(fig)


def histo_discos(discos,num_subdiv):
    """`histo_discos(discos,tiempos,tmax,newt)`

    Esta función crea un histograma de las posiciones de los centros a lo largo del eje x.

    Args:
        discos (Disco): Son todas las caracteristicas de los discos    inicializadas en la clase Disco.
        num_subdiv (float): Representa el número de subdivisiones
    """
    path = os.getcwd()
    plt.style.use('default')
    posiciones_x = np.concatenate([disco.arrayposicionx for disco in discos])

    plt.hist(posiciones_x,num_subdiv,color = [0,1,1], rwidth=0.9)
    plt.title('Distribucion de las posiciones de los discos')
    plt.xlabel('Posiciones en x')
    plt.ylabel('Numero de discos')
    plt.savefig(os.path.join(path, f"histograma.png"))


def crear_video(fps):
    """`crear_video(fps)`

    Esta función crea un video del movimiento de las partículas en la grilla.

   Args:
        fps (int): Los fps del video.
    """

    path = os.getcwd()
    filenames = sorted(glob.glob(os.path.join(path, "fotograma*.png")))
    clip = ImageSequenceClip(filenames, fps=fps)
    clip.write_videofile(f"{path}/video_colision.mp4", fps=fps)
    for filename in glob.glob(os.path.join(path, "fotograma*.png")):
        os.remove(filename)
