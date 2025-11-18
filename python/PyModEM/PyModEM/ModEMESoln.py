import struct
from dataclasses import dataclass
import numpy as np


@dataclass
class ESolnData:
    gridType : str
    nx : int
    ny : int
    nz : int
    x : np.ndarray
    y : np.ndarray 
    z : np.ndarray

class ESoln:
        
    def __init__(self, data=None, fname=None):

        if data is None:
            self._data = ESolnData(
                gridType=None,
                nx=0,
                ny=0,
                nz=0,
                x=None,
                y=None,
                z=None
            )

        if data is not None and fname is None:
            self._data = data

        if fname is not None:
            self.read(fname)


    def __sub__(self, other):
        return ESoln(ESolnData(
            'EDGE',
            nx=self.nx - other.nx,
            ny=self.ny - other.ny,
            nz=self.nz - other.nz,
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z
        ))

    @property
    def nx(self) -> int:
        return self._data.nx

    @property
    def ny(self) -> int:
        return self._data.ny

    @property
    def nz(self) -> int:
        return self._data.nz

    @property
    def gridType(self) -> str:
        return self._data.gridType

    @property
    def x(self) -> np.ndarray:
        return self._data.x

    @property
    def y(self) -> np.ndarray:
        return self._data.y

    @property
    def z(self) -> np.ndarray:
        return self._data.z

    def read(self, fname):
        with open(fname, 'rb') as file:
            _ = struct.unpack('i', file.read(4)) # Fortran record header - skip
            self._data.nx = struct.unpack('i', file.read(4))[0]
            self._data.ny = struct.unpack('i', file.read(4))[0]
            self._data.nz = struct.unpack('i', file.read(4))[0]
            self._data.gridType = str(file.read(80).decode('utf-8'))

            _ = struct.unpack('i', file.read(4)) # Fortran record handle - skip
            xs = struct.iter_unpack('D', file.read(self.nx*16))
            ys = struct.iter_unpack('D', file.read(self.ny*16))
            zs = struct.iter_unpack('D', file.read(self.nz*16))

            self._data.x = np.array([x[0] for x in xs])
            self._data.y = np.array([y[0] for y in ys])
            self._data.z = np.array([z[0] for z in zs])

    def write(self, fname):
        with open(fname, 'w') as file:
            file.write(str(self.nx) + '\n')
            file.write(str(self.ny) + '\n')
            file.write(str(self.nz) + '\n')
            file.write(self.gridType + '\n')

            np.savetxt(file, self.x, delimiter=',')
            file.write('\n')
            np.savetxt(file, self.y, delimiter=',')
            file.write('\n')
            np.savetxt(file, self.z, delimiter=',')

        return fname