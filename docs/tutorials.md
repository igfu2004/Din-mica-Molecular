# Ejemplo de uso 

Si queremos utilizar el código para realizar una simulación de la colisión entre discos, además de realizar un histograma con las posiciones en el eje x de los discos durante el tiempo establecido, debemos definir los valores que queremos utilizar mediante el archivo `main.py`. 

---
## Bibliotecas necesarias
Debemos tener en cuenta que las siguientes bibliotecas deben estar instaladas:

- `numpy`
- `matplotlib`
- `moviepy`


Si se está utilizando `bash`, se pueden instalar con: 

```bash 
pip install numpy matplotlib moviepy 
```

Además, debemos importar las bibliotecas necesarias en el código de la siguiente manera:
```python 
import numpy as np
import matplotlib.pyplot as plt
from random import uniform as uf
from moviepy.editor import *
import glob
import os
```

Luego, en el archivo `main.py` procedemos a establecer los parámetros con los que queremos trabajar:

Asumamos que queremos llevar a cabo la simulación de colisiones elásticas con 10 discos distribuidos de manera aleatoria en una caja con dimensiones 1x1, con colores también aleatorios. Además, queremos observar visualmente la simulación mediante un video de 30 segundos.

En el archivo `main.py`, vamos a importar las clases y funciones que se definieron en los archivos `clases.py` y `funciones.py`, cuyo contenido con su respectiva documentación se encuentra en el apartado de [reference](reference.md).

```python 
from clases import Disco, Box, Grilla
from funciones import *
```

Podemos establecer las dimensiones de la caja según se necesite:
```python 
ladohorizontal = 1
ladovertical = 1
```

Luego, definimos los parámetros que se requieran para los discos además del tiempo de simulación en segundos:
```python
numero_discos = 10
masa = 1
radio = 0.05
velomax = 0.2
tmax = 30
```

Luego, creamos los elementos del sistema que vamos a estudiar. Es importante tomar en cuenta que en este caso estamos llamando a las clases del archivo `clases.py` y a una función del archivo `funciones.py` para inicializar los discos, estos discos se guardan en una lista que vamos a necesitar para las funciones que manejan la colisión y las gráficas. Es importante que existen distintas opciones para cómo se inicializan los discos. En los últimos dos parámetros de la
función, al poner `True` en ambos estamos solicitando que la distribución de los discos en la grilla y sus colores sean aleatorios. Se podría escoger que no sea así, en ese caso se debería escribir específicamente cuáles posiciones queremos y cuáles colores queremos que tengan los discos, lo cual se haría accediendo a los discos mediante la lista de ellos y definiendo los atributos que queremos fijos.  
```python 
discos = [] 
caja = Box(ladohorizontal, ladovertical) 
grilla = Grilla(caja.longitudx,caja.longitudy,radio) 
discos = inicializacion_discos(radio, masa, -velomax, velomax, grilla, numero_discos, True, True)
```

Para la evolución temporal del sistema, debemos definir la cantidad de fotogramas por segundo `FPS`, debemos asegurarnos que sean suficientes de manera que el sistema pueda llevarse a cabo de manera adecuada, además definimos el tiempo que habrá entre fotogramas `newt`. Luego, mediante un `for loop`, procedemos a llevar a cabo la evolución, actualizando la posición de los discos en cada fotograma `n` mediante otro `for loop` donde se toma la posición de cada disco y se utiliza la función de `funciones.py` que realiza la
asignación de la nueva posición para el disco. Luego, por cada fotograma se lleva a cabo la funcion `colision_proxima` que gestiona todo el sistema de colisiones. Luego, para efectos de la visualización mediante un video, graficamos los discos mediante la función `graf_discos` (de nuevo en cada fotograma) e incrementamos el fotograma para que se pase a la siguiente iteración. 
```python 
FPS = 60
newt = 1/FPS

fotograma = 0
for n in range(0,tmax*FPS):
    for i in range(numero_discos):
        discos[i] = nueva_posicion(discos[i],newt)

    discos = colision_proxima(grilla,discos, cambio_velocidad_colision_pares,newt,manejo_de_colisiones_pares,tiempo_colision_pared,deteccion_colision_pared_con_manejo,caja.longitudx,caja.longitudy)
    graf_discos(discos,caja,fotograma,grilla)
    fotograma += 1

crear_video(FPS)
```

Por último, se puede realizar un histograma con las posiciones en el eje x de los discos durante el tiempo que se dio la dinámica. Para obtener mejores resultados en el histograma, se recomienda utilizar una cantidad de discos elevada. Considerando esto, es mejor no llevar a cabo la graficación ni el video de los discos, es decir sería mejor descartar la visualización de las colisiones, esto porque son las secciones del código que toman más tiempo e implicaría un gran
costo realizarlas con una gran cantidad de discos. 

Por lo tanto, se procedería a comentar las siguientes líneas en el `main.py`:
```python 
#graf_discos(discos,caja,fotograma,grilla)
#fotograma += 1
 
#crear_video(FPS)
```
Además, en los parámetros de los discos que definimos anteriormente, cambiaríamos los valores del número de discos, además del radio (se necesitaría un menor radio ya que tenemos mayor cantidad de discos). Luego, para crear el histograma simplemente llamamos la función para esto del archivo `funciones.py`:
```python 
histo_discos(discos,caja.longitudx,50)
```

### Ejemplo de Simulación
A continuación, podemos observar un ejemplo del video que se obtendría utilizando los valores que definimos anteriormente:
<video width="300" height="200" controls>
  <source src= "https://github.com/igfu2004/Din-mica-Molecular/raw/main/docs/video_ejemplo.mp4" type="video/mp4">
  Tu navegador no soporta el elemento de video.
</video>

### Ejemplo de histogramas
A continuación, veremos un ejemplo para el resultado de histograma con 4 discos de radio 0.09, durante una simulación de 60 segundos.

<img src="https://github.com/igfu2004/Din-mica-Molecular/raw/main/docs/histo004.png" alt="Histograma de las posiciones en x para 100 discos" width="600"/>


