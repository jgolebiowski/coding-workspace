import ctypes

#Load a ahsred library under that address
testlib = ctypes.CDLL("testlib.so")

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
