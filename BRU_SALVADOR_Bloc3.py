"""
BRU_SALVADOR_matriz
    Generació de la matriu de confusió en un fitxer .txt que es genera en el directori de treball.

Usage:
    BRU_SALVADOR_matriz.py [options] <directori_Avaluacio> <directori_Train>

Options:
    --distancia=<ds>    Valor entero: 0=Euclidiana 1=Manhattan      [default: 0]
    --help, -h          Mostrar este mensaje de ayuda
"""

from docopt import docopt
import Funcions
import h5py
import os
import numpy as np
from MatConf import MatConf

if __name__ == '__main__':
    args = docopt(__doc__)

    avaluacio = args['<directori_Avaluacio>']  #direcció on esta la imatge
    train = args['<directori_Train>']
    distancia = int(args['--distancia'])

    if distancia not in [0, 1]:
        print('Error en distancia. {distancia} no es un booleano.'.format(distancia=distancia))

    matriz = MatConf()


    for dPath, dNames, files in os.walk(avaluacio):

        for fil in files:
            with h5py.File(os.path.join(avaluacio, fil), 'r') as hf:
                dsetA = hf.get('name')
                nomA = dsetA.attrs['name']  # extreu els noms
                dataA = np.array(hf.get('vects'))  # extreu els vectors)

            for z in dataA:
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
                                dis = Funcions.BRU_SALVADOR_distancia_euclidiana(z, i)
                            elif distancia == 1:
                                dis = Funcions.BRU_SALVADOR_distancia_manhattan(z, i)
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

                    if num1 >=25:
                        matriz.meteConf(nomA, 'ZNI')
                    elif nom1==nom2==nom3:
                        #el nom unic
                        matriz.meteConf(nomA, nom1)
                    elif num1 <= 3:
                        matriz.meteConf(nomA, nom1)
                    elif num1*1.1 <= num2:
                        matriz.meteConf(nomA, nom1)
                    elif nom1==nom2:
                        #el nom de 1 i 2
                        matriz.meteConf(nomA, nom1)
                    elif nom1==nom3:
                        # el nom de 1 i 3
                        matriz.meteConf(nomA, nom1)
                    elif nom2 == nom3:
                        # el nom de 2 i 3
                        matriz.meteConf(nomA, nom2)
                    else:
                       matriz.meteConf(nomA, 'ZNI')

                else:

                    if num1 >=35:
                        matriz.meteConf(nomA, 'ZNI')
                    elif nom1==nom2==nom3:
                        #el nom unic
                        matriz.meteConf(nomA, nom1)
                    elif num1 <= 9:
                        matriz.meteConf(nomA, nom1)
                    elif num1*1.1 <= num2:
                        matriz.meteConf(nomA, nom1)
                    elif nom1==nom2:
                        #el nom de 1 i 2
                        matriz.meteConf(nomA, nom1)
                    elif nom1==nom3:
                        # el nom de 1 i 3
                        matriz.meteConf(nomA, nom1)
                    elif nom2 == nom3:
                        # el nom de 2 i 3
                        matriz.meteConf(nomA, nom2)
                    else:
                       matriz.meteConf(nomA, 'ZNI')


    A = matriz.save()
    with open('Matriz.txt', 'w') as out:
        out.write(str(A))

    #Comprovació de Paràmetres: Matriu i Eficiència
    #matriz.print()
    #matriz.eff()
