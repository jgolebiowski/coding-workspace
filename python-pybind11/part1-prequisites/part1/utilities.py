"""Some utilities for wrapping"""
from cffi import FFI
import os

# Load the shared library
ffi = FFI()
lib = ffi.dlopen(os.path.dirname(__file__) + "/lib/libpart1_intro.dylib")
print('Loaded lib {0} from {1}'.format(lib, __name__))

ffi.cdef("""
/*
------
Utilities.h
------
*/

/* Print hello world */
void hello_world();

/* Print hello world with openMP parallelism */
void hello_world_omp();

/*
------
Interface.h
------
*/

/* Define a return tuple structure */
struct returntuple_1d
{
    int size;
    double * data;
};

/* Initialize a vctor and return the tuple representation */
struct returntuple_1d initialize_vector(int size);
""")

def hello_world():
    """
    Print Hello world from cpp
    """
    lib.hello_world()

def hello_world_omp():
    """
    Print Hello world from cpp
    """
    lib.hello_world_omp()
