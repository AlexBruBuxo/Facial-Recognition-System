
"""
BRU_SALVADOR_Bloc1
    Crea fitxers .bin amb vectors DCT a partir d'un directori origen amb
    imatges de cares a nivell de gris.
    Manté l'estructura original de fitxers.
Usage:
    creaModeloGlobal.py [options] <origen> <destino>

Options:
    --dimImg=<wd>  Reescalar las imágenes a esta anchura  [default: 45]
    --numCof=<nc>  Número de coeficientes del vector      [default: 78]
    --help, -h     Mostrar este mensaje de ayuda
"""


import os
import imageio
from docopt import docopt
import Funcions
from Modelo import Modelo


if __name__ == '__main__':
    args = docopt(__doc__)

    origen = args['<origen>']
    destino = args['<destino>']
    dimImg = int(args['--dimImg'])
    numCof = int(args['--numCof'])

    os.mkdir(destino)

    longOrigen = len(origen)
    for dirpath, dirnames, filenames in os.walk(origen):
        #creamos directorios indicados por dirnames
        subDirOrigen = dirpath[longOrigen+1:] #+1 pk no queremos copiar el origen del path
        modelo=Modelo(subDirOrigen)
        for file in filenames:
            extension = os.path.splitext(file)[1]
            if extension[1:] in ('jpg', 'JPG', 'png', 'PNG'):
                imagen = imageio.imread(os.path.join(dirpath, file))
                params = Funcions.BRU_SALVADOR_extract_features(imagen, dimImg, numCof)
                modelo.add(params)
        if len(subDirOrigen) != 0:
            modelo.save(os.path.join(destino, subDirOrigen) + '.bin')