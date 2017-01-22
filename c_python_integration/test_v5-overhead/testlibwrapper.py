from cffi import FFI
import numpy as np

# Random function
def get_oned_array(rows):
    array = np.zeros(rows)
    for i in range(rows):
        array[i] = i
    return array

def get_twod_array(rows, cols):
    array = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            array[i,j] = i * cols + j
    return array


def cast_matrix_v2(matrix):
    # Create an array of pointers to a double with the no of entries = no of rows
    ap = ffi.new("double* [%d]" % (matrix.shape[0]))
    # Each of the entries to the array of pointers is a row of the original np array
    for i in range(matrix.shape[0]):
        ap[i] = ffi.cast("double *", matrix[i].ctypes.data)
    return ap

def cast_matrix(matrix):
    # Create an array of pointers to a double
    ap = ffi.new("double* [%d]" % (matrix.shape[0]))
    # Create a pointer to the numpy array
    ptr = ffi.cast("double *", matrix.ctypes.data)
    # Each of the pointers in the previously created array of poinyers 
    # Is set to be a pointer to one of the columns of the numpy array
    # By shifting (off-setting) the original pointer to [0][0] in memory
    for i in range(matrix.shape[0]):
        ap[i] = ptr + i*matrix.shape[1]                                                  
    return ap


# Define an instance of ffi
ffi = FFI()

# Define the functions (header)
ffi.cdef("""
void hello_world(void);
int return_int(int);
void call_speed(double *, int);
double cube(double);
void one_d_array(double *, int);
""")

#Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ffi.dlopen(MYDIR+"/testlib.so")

# Call a function from that library
testlib.hello_world()

#------  Prepare the function definitions
def c_cube(number):
    c_number = ffi.cast("double", number)
    return testlib.cube(c_number)

C_return = c_cube(10)

print C_return, type(C_return)

#----- Definition for the array function
def c_array_cube(array):
    rows = array.shape[0]
    c_array = ffi.cast("double *", array.ctypes.data)
    testlib.one_d_array(c_array, rows)

#----- Define a hybrid function
def hybrid_funct(arr):
    length = len(arr)
    for i in range(length):
        arr[i] = c_cube(arr[i])


def hybrid_funct_v2(array):
    rows = array.shape[0]
    c_array = ffi.cast("double *", array.ctypes.data)
    for i in range(len(array)):
        testlib.cube(c_array[i])


#------ Same thing with ctypes

import ctypes
testlib_ctypes = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")

testlib_ctypes.return_int.restype = ctypes.c_int
testlib_ctypes.return_int.argtypes = [ctypes.c_int]

