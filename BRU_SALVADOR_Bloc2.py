"""
BRU_SALVADOR_Bloc2
    Retorna el nom de la persona de test més semblant a la imatge d'entrada original (sense preocessat prèvi).

Usage:
    BRU_SALVADOR_Bloc2.py [options] <directori_Imatge> <directori_Train>

Options:
    --distancia=<ds>    Valor entero: 0=Euclidiana 1=Manhattan      [default: 0]
    --dimImg=<wd>  Reescalar las imágenes a esta anchura  [default: 45]
    --numCof=<nc>  Número de coeficientes del vector      [default: 78]
    --help, -h          Mostrar este mensaje de ayuda
"""

from docopt import docopt
import Funcions
import h5py
import os
import numpy as np
import matplotlib.image as mpimg

if __name__ == '__main__':
    args = docopt(__doc__)

    imatge = args['<directori_Imatge>']  #direcció on esta la imatge
    train = args['<directori_Train>']
    distancia = int(args['--distancia'])
    dimImg = int(args['--dimImg'])
    numCof = int(args['--numCof'])

    if distancia not in [0, 1]:
        print('Error en distancia. {distancia} no es un booleano.'.format(distancia=distancia))

    ima = mpimg.imread(imatge)
    ima = Funcions.BRU_SALVADOR_detectaCara2gris(ima)
    v = Funcions.BRU_SALVADOR_extract_features(ima, dimImg, numCof)

    dist = list()

    for dirpath, dirnames, filenames in os.walk(train):
        for file in filenames:
            with h5py.File(os.path.join(train, file), 'r') as hf:
                dsetT = hf.get('name')
                nomT = dsetT.attrs['name']  # extreu els noms
                dataT = np.array(hf.get('vects'))  # extreu els vectors)

            vec = list()
            for i in dataT:
                if distancia == 0:
                    dis = Funcions.BRU_SALVADOR_distancia_euclidiana(v, i)
                elif distancia == 1:
                    dis = Funcions.BRU_SALVADOR_distancia_manhattan(v, i)
                vec.append(dis)
            vec.sort()
            vec = vec[0:3]

            for i in range(len(vec)):
                dist.append((vec[i], nomT))

    dist.sort()
    dist = dist[0:3]

    num1, nom1 = dist[0]
    num2, nom2 = dist[1]
    num3, nom3 = dist[2]

    if distancia == 0:
        if num1 >= 25:
            print('No identificat.')
        elif nom1 == nom2 == nom3:
            print(nom1)
        elif num1 <= 3:
            print(nom1)
        elif num1 * 1.1 <= num2:
            print(nom1)
        elif nom1 == nom2:
            print(nom1)
        elif nom1 == nom3:
            print(nom1)
        elif nom2 == nom3:
            print(nom2)
        else:
            print('No identificat.')
    else:
        if num1 >= 35:
            print('No identificat.')
        elif nom1 == nom2 == nom3:
            print(nom1)
        elif num1 <= 9:
            print(nom1)
        elif num1 * 1.1 <= num2:
            print(nom1)
        elif nom1 == nom2:
            print(nom1)
        elif nom1 == nom3:
            print(nom1)
        elif nom2 == nom3:
            print(nom2)
        else:
            print('No identificat.')