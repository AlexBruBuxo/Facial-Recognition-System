import os
import shutil
import imageio
import numpy as np
import matplotlib.image as mpimg
from docopt import docopt
import dlib
from Funcions import BRU_SALVADOR_im2gris

def cpR2g(origen, destino):
    '''
    cpR2g
        Copia recursiva d'un directori a un destí que no ha d'existir prèviament
        un conjunt d'imatges, que passa a nivell de gris i extreu la cara.

    Usage:
        cpR2g [ -h | --help] ORIGEN DESTINO

    Options:
        -h, --help  muestra esta ayuda
    '''

    #compprobar que el directorio es un directorio:
    if not os.path.isdir(origen):
        print('Error en cpR2g: {origen} no es un directorio'.format(origen=origen))
        return None

    #comprobamos que el destino no existe
    if os.path.exists(destino):
        print('Error en cpR2g: {destino} ya existe'.format(destino=destino))

    #crear directorio:
    else:
        os.mkdir(destino)

    longOrigen = len(origen)
    for dirpath, dirnames, filenames in os.walk(origen):
        #creamos directorios indicados por dirnames
        subDirOrigen = dirpath[longOrigen+1:] #+1 pk no queremos copiar el origen del path
        for directorio in dirnames:
            os.mkdir(os.path.join(destino, subDirOrigen, directorio)) #encadena los nombres con la logica de paths (las barras '\' correctas)
        #ahora copiamos ficheros
        for fichero in filenames:
            y = mpimg.imread(os.path.join(dirpath, fichero))
            y = np.uint8(BRU_SALVADOR_im2gris(y))

            #detectar cara amb el dlib
            detector=dlib.get_frontal_face_detector()
            d=detector(y,1) #coordenades de la posició on esta la cara
            if len(d)!=0:
                cara = y[d[0].top():d[0].bottom(), d[0].left():d[0].right()]
                imageio.imsave(os.path.join(destino, subDirOrigen, fichero), cara, 'jpg')
            else:
                print('Hi ha una imatge (fichero) sense cara'.format(fichero=fichero))
            #shutil.copy(os.path.join(dirpath, fichero), os.path.join(destino, subDirOrigen, fichero))

if __name__=='__main__':
    opciones = docopt(cpR2g.__doc__)

    cpR2g(opciones['ORIGEN'], opciones['DESTINO'])