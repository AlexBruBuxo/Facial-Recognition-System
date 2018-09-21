from skimage import transform
from scipy.fftpack import dct
import numpy as np
import dlib
import os

def BRU_SALVADOR_im2gris(image):
    y = 0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]
    return y

def BRU_SALVADOR_detectaCara2gris(imatge):
    y = np.uint8(BRU_SALVADOR_im2gris(imatge))
    detector = dlib.get_frontal_face_detector()
    d = detector(y, 1)  # coordenades de la posició on esta la cara
    cara = y[d[0].top():d[0].bottom(), d[0].left():d[0].right()]
    return cara

def BRU_SALVADOR_ordenaDCT(x, num_coef): #x es la matriu amb els coeficients dct, num_coef és el tamany del vector a retornar
    '''
    Funció que retorna un vector amb els coeficients de la dct ordenats de frecuencia més baia a més alta
    fins a la meitat dels valors (diagonal central)
    '''
    y=list()
    arrdim=np.shape(x)
    for i in range(1,arrdim[0]+1):  #recorrem les diagonals de baix a dalt, fins a la diagonal central
        llista=list()
        for j in range(i):
            llista.append(x[i-j-1,j])
        if i%2!=0: #reordenem les llistes imparells 8que segons la nomenclatura del for de 'i' són les parells
            llista.reverse()
        y.append(llista)
    #ajuntem les llistes
    vector=list()
    for i in range(len(y)):
        vector=vector+y[i]
    return vector[0:num_coef]


def BRU_SALVADOR_extract_features(ima, ample=40, num_coef=45):   #num_coef=45 per mantenir diagonals completes (una diagonal incompleta genera asimetria)
    ima = transform.resize(ima, (ample, ample), mode='reflect')
    X=dct(ima, type=2, axis=0, norm='ortho')
    X=dct(X, type=2, axis=1, norm='ortho')
    vector=BRU_SALVADOR_ordenaDCT(X, num_coef)
    return vector

def BRU_SALVADOR_distancia_euclidiana(a, b):
    '''
    Funció que retorna la distancia euclidiana entre dos vectors de mateiz numero de coeficients.
    '''
    distancia=0
    for i in range (len(a)):
        distancia += (a[i] - b[i]) ** 2
    return distancia

def BRU_SALVADOR_distancia_manhattan(a, b):
    '''
    Funció que retorna la distancia de manhattan entre dos vectors de mateix numero de coeficients.
    '''
    distancia = 0
    for i in range (len(a)):
        distancia += abs(a[i] - b[i])
    return distancia

def BRU_SALVADOR_extreuNom(fitxer):
    pos = fitxer.find('.')
    return fitxer[:pos]

def BRU_SALVADOR_creaModeloGlobal(origen, destino, dimImg=40, numCof=45):
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