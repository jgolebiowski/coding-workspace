from cffi import FFI
import numpy as np


# Define an instance of ffi
ffi = FFI()

# Define the functions (header)
ffi.cdef("""
void hello_world(void);
double addition(double, double);
void twod_array_pointer_2_pointer(double **, int, int);
void numpy_array_operation(double *, int, int);
""")

#Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ffi.dlopen(MYDIR+"/testlib.so")

# Call a function from that library
testlib.hello_world()

#------  Prepare data types for a simple function
# Define python data
A = 1
B = 2

# Cast the data as C++ data
C_A = ffi.cast("double", A)
C_B = ffi.cast("double", B)

# Call the function
C_return = testlib.addition(C_A, C_B)

# Alternatively 
# c_return = testlib.addition(ffi.cast("double", A), ffi.cast("double", B))

print C_return, type(C_return)

#------  Parse a numpy array to c++ as a 1d array
print "V1\nParse a numpy array to c++ as a 1d array"
# Define the Python array
testarr = np.zeros(( 3, 4))
rows, cols = testarr.shape
testarr[0,2] = 2
print testarr
print "c++"

# Cast the array as a c++ pointer 
c_testarr = ffi.cast("double *", testarr.ctypes.data)
# Call the function
testlib.numpy_array_operation(c_testarr, rows, cols)

# Alternatively 
# testlib.numpy_array_operation( ffi.cast("double *", testarr.ctypes.data), rows, cols)

print "After C++"
print type(c_testarr), c_testarr[0]
print type(testarr), testarr

#------ Parse a numpy array ass a **double to a c++ function
print "V2\nParse a numpy array ass a **double to a c++ function"
# Define the Python array
testarr = np.zeros(( 3, 4))
rows, cols = testarr.shape
testarr[0,2] = 2
print testarr
print "c++"

# Define a function that converts the data 
def cast_matrix(matrix, ffi):
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


def function_wrapper(testarr):
    # Function wrapper makes sense since Python will delete 
    # te c_pp_testarr after the call
    c_pp_testarr = cast_matrix(testarr, ffi)
    testlib.twod_array_pointer_2_pointer(c_pp_testarr, rows, cols)

function_wrapper(testarr)
print "After C++"
#print type(c_pp_testarr), c_pp_testarr[0][0]
print type(testarr), testarr

#------  Parse a numpy array to c++ as a **double in in form of an 1d array of pointers ot columns
print "V3\nParse a numpy array to c++ as a **double in form of an 1d array of pointers ot columns"
# Define the Python array
testarr = np.zeros(( 3, 4))
rows, cols = testarr.shape
testarr[1,2] = 2
print testarr
print "c++"

# Define a function that converts the data, 
# passing ffi to the function is optional
def cast_matrix_v2(matrix, ffi):
    # Create an array of pointers to a double with the no of entries = no of rows
    ap = ffi.new("double* [%d]" % (matrix.shape[0]))
	# Each of the entries to the array of pointers is a row of the original np array
    for i in range(matrix.shape[0]):
        ap[i] = ffi.cast("double *", matrix[i].ctypes.data) 
    return ap


def function_wrapper(testarr):
    # Function wrapper makes sense since Python will delete 
    # te c_pp_testarr after the call
    c_pp_testarr = cast_matrix_v2(testarr, ffi)
    testlib.twod_array_pointer_2_pointer(c_pp_testarr, rows, cols)

function_wrapper(testarr)


print "After C++"
#print type(c_pp_testarr), c_pp_testarr[0][0]
print type(testarr), testarr

