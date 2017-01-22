import numpy as np
import ctypes

#Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")

#Test the library
testlib.hello_world()

# Define function
square_matrix = testlib.square_matrix
square_matrix.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                          ctypes.c_int, 
                          ctypes.c_int]
square_matrix.restypes = None

def squareMatrix(mat):
    rows, cols = mat.shape
    square_matrix(mat, rows, cols)

square_array = testlib.square_array
square_array.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                          ctypes.c_int, 
                          ctypes.c_int]
square_array.restypes = None

def squareArray(mat):
    rows, cols = mat.shape
    square_array(mat, rows, cols)


# Declare matrix
n = 1000
ns = n*n
A = np.arange(ns, dtype="float64")
A.shape = (n, n)




###############################################################################
# Old version of defining stuff:

# square_matrix2 = testlib.square_matrix
# square_matrix2.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
# square_matrix2.restypes = None

# def square_matrix_2(mat, rows, cols):
#     B = mat.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
#     square_matrix2(B, rows, cols)