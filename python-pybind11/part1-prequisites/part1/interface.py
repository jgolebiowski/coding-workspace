"""Some utilities for wrapping"""
from cffi import FFI
import os
import numpy as np

# Load the shared library
ffi = FFI()
lib = ffi.dlopen(os.path.dirname(__file__) + "/lib/libpart1_intro.dylib")
print('Loaded lib {0} from {1}'.format(lib, __name__))

ffi.cdef("""
/*
------
Interface.h
------
*/

/* Define a return tuple structure */
struct myarray
{
    int n_rows;
    int n_cols;
    double * data;
};

/* Initialize a 2dmatrix and return the tuple representation */
struct myarray myarray_construct(int nRows, int nCols);
""")

def get_vector(size):
    """return a vector from cpp
    """
    ret = lib.myarray_construct(size, size)
    return _asarray(ret.data, (ret.n_rows, ret.n_cols))


ctypes2nptypes = dict(int=np.intc,
                      float=np.float32,
                      double=np.float64)

def _asarray(datapointer, shape):
    """
    Interpret a buffer as an array

    Parameters
    ----------
    datapointer :  _cffi_backend.CData
        Pointer to a c-array from numpy
    shape : int or tuple
        shape of the array

    Returns
    -------
    ndarray
        Array with the data
    """
    if isinstance(shape, tuple):
        size = 1
        for item in shape:
            size *= item
    else:
        size = shape


    # Get the datatype
    T = ffi.getctype(ffi.typeof(datapointer).item)
    if T not in ctypes2nptypes:
        raise RuntimeError("Cannot create an array for element type: {}".format(T))

    # Wrap the buffer in a numpy array
    buffer = ffi.buffer(datapointer, size * ffi.sizeof(T))
    return np.frombuffer(buffer, dtype=ctypes2nptypes[T]).reshape(shape)
