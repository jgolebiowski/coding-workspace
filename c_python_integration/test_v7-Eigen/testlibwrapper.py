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
square_matrix.restype = None

def squareMatrix(mat):
    rows, cols = mat.shape
    square_matrix(mat, rows, cols)

square_array = testlib.square_array
square_array.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                          ctypes.c_int, 
                          ctypes.c_int]
square_array.restype = None

def squareArray(mat):
    rows, cols = mat.shape
    square_array(mat, rows, cols)


square_eMatrix = testlib.square_eMatrix
square_eMatrix.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                          ctypes.c_int, 
                          ctypes.c_int]
square_eMatrix.restype = None

def squareEMatrix(mat):
	rows, cols = mat.shape
	square_eMatrix(mat, rows, cols)


square_ret_eMatrix = testlib.return_eMatrix
square_ret_eMatrix.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
								np.ctypeslib.ndpointer(dtype=ctypes.c_double),
								ctypes.c_int, 
								ctypes.c_int]
square_ret_eMatrix.restype = None

def squareRetEMatrix(mat):
	rows, cols = mat.shape
	retmat = np.empty_like(mat)
	square_ret_eMatrix(mat, retmat, rows, cols)
	return retmat

multiply_eMatrix = testlib.multiply_eMatrix
multiply_eMatrix.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double),
								np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
								np.ctypeslib.ndpointer(dtype=ctypes.c_double),
								ctypes.c_int, 
								ctypes.c_int]
multiply_eMatrix.restype = None

def multiplyEMatrix(mat1, mat2):
	rows, cols = mat1.shape
	retmat = np.empty_like(mat1)
	multiply_eMatrix(mat1, mat2, retmat, rows, cols)
	return retmat



# Declare matrix
n = 1000
ns = n*n
A = np.arange(ns, dtype="float64")
B = np.arange(ns, dtype="float64")
A.shape = (n, n)
B.shape = (n, n)




###############################################################################
# Old version of defining stuff:

# square_matrix2 = testlib.square_matrix
# square_matrix2.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int]
# square_matrix2.restypes = None

# def square_matrix_2(mat, rows, cols):
#     B = mat.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
#     square_matrix2(B, rows, cols)