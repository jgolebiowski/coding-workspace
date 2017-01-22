from cffi import FFI
import numpy as np


# Define an instance of ffi
ffi = FFI()

# Define the functions (header)
ffi.cdef("""
void twod_array_p2p_print(double **, int, int);
void matrix_elements_operation(double **, int, int);
""")

#Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ffi.dlopen(MYDIR+"/testlib.so")

#------ Define the function wrapper 
# Define a function that converts the data, 
# passing ffi to the function is optional
def cast_matrix(matrix, ffi):
    # Create an array of pointers to a double with the no of entries = no of rows
    ap = ffi.new("double* [%d]" % (matrix.shape[0]))
	# Each of the entries to the array of pointers is a row of the original np array
    for i in range(matrix.shape[0]):
        ap[i] = ffi.cast("double *", matrix[i].ctypes.data) 
    return ap

# Function wrapper makes sense since Python will delete 
# te c_pp_testarr after the call
def matrix_elements_pow__wrapped(np_array):
    c_pp_testarr = cast_matrix(np_array, ffi)
    rows, cols = np_array.shape
    testlib.matrix_elements_operation(c_pp_testarr, rows, cols)



# Define the Python array
testarr = np.zeros(( 10,10 ))
for i in range(testarr.shape[0]):
    for j in range(testarr.shape[1]):
        testarr[i][j] = testarr.shape[1] * i + j

print testarr
matrix_elements_pow__wrapped(testarr)

print "After C++"
print testarr
