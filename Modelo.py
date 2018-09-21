import numpy as np
import h5py
import os

class Modelo:
    def __init__(self, nombre):
        self.__name = nombre
        self.__data = []

    def add(self, vector):
        self.__data.append(vector)

    __add__ = add   # para permitir cosas como m += [1, 2, 3]

    def save(self, ficMod):
        with h5py.File(ficMod, 'w') as hf:
            # La escritura de cadenas de texto es de lo más
            # complicado de h5py.
            # Ver http://docs.h5py.org/en/latest/strings.html
            dt = h5py.special_dtype(vlen = bytes)
            dset = hf.create_dataset('name', (100,), dtype = dt)
            dset.attrs['name'] = self.__name

            # La escritura de ndarrays es mucho más sencilla
            hf.create_dataset('vects', data = self.__data)

    def load(self, ficMod):
        with h5py.File(ficMod, 'r') as hf:
            dset = hf.get('name')
            self.__name = dset.attrs['name']
            self.__data = np.array(hf.get('vects'))

