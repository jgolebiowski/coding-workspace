import ctypes
import numpy as np



#Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")

# Call a function from that library
testlib.hello_world()

#Specify the response type and the argument types for that function, necessary if not C ints
testlib.addition.restype = ctypes.c_double
testlib.addition.argtypes = [ctypes.c_double, ctypes.c_double]

A = 1.0
B = 10.0
value = testlib.addition(A, B)
print value


print type(value)
print type(testlib)
print type(testlib.addition)


#------ Passing a numpy array as a 1d array to C

# Define the output type as None
testlib.numpy_array_operation.restype = None
# Define translation from a numpy array to a C pointer 
c_pass_arr = np.ctypeslib.ndpointer(dtype=ctypes.c_double, flags= "C_CONTIGUOUS")
# Define the input to the function as a pointer and two ints 
testlib.numpy_array_operation.argtypes = [c_pass_arr, ctypes.c_int, ctypes.c_int]

testarr = np.zeros( (3,4))
rows, cols =  testarr.shape
print rows, cols

testarr[0,2] = 2
print testarr
print "C++"
#Call the function
testlib.numpy_array_operation(testarr, rows, cols)
print testarr


# #------ Passing a numpy array as a pointer to a pointer - Not working
# 
# # Define the output type as None
# testlib.twod_array_pointer_2_pointer.restype = None
# # Define translation from a numpy array of pointers to a pointer to a pointer
# c_pass_arr_pp = np.ctypeslib.ndpointer(dtype=np.uintp, flags= "C_CONTIGUOUS")
# 
# # Define the numpy array
# testarr = np.zeros( (3,4))
# rows, cols =  testarr.shape
# testarr[0,2] = 2
# # Redefine the numpy array as a numpy array of pointers
# # testarr.ctypes.data points to testarr[0][0] place in memory
# # testarr.shape gives the shape in units
# # testarr.strides gives the number of locations in memory between beginnings of successive array elements, measured in bytes or in units of the size of the array's elements (strides of memory)
# # It essentially defines an np.array(testarr.shape[0]), from 0 to testarr.shape[0] with the step of 1
# # Multiplies every entry by the number of locations in memory of a single rr entry, and
# # Adds the position of the [0][0] memory ( testarr.cytpes.data + ) to every entry
# # And gives that objecvt as a pointer
# testarr_pp = (testarr.ctypes.data + (np.arange(testarr.shape[0]) * testarr.strides[0])).astype(np.uintp)
# 
# print "test"
# print testarr.ctypes.data
# # Define the input to the function as a pointer and two ints 
# testlib.numpy_array_operation.argtypes = [c_pass_arr_pp, ctypes.c_int, ctypes.c_int]
# 
# print "C++"
# #Call the function
# testlib.numpy_array_operation(testarr_pp, rows, cols)
