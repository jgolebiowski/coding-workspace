import numpy as np
import ctypes

# Load a ahsred library under that address
from os import getcwd
MYDIR = getcwd()
testlib = ctypes.cdll.LoadLibrary(MYDIR + "/mylibrary.so")

# Test the library
testlib.hello_world()

# Define test function
cpp_squareArray = testlib.square_array
cpp_squareArray.argtypes = [np.ctypeslib.ndpointer(dtype=ctypes.c_double),
                            ctypes.c_int,
                            ctypes.c_int]
cpp_squareArray.restypes = None


def squareArray(mat):
    rows, cols = mat.shape
    cpp_squareArray(mat, rows, cols)


# Define function parameters
# // Initialize an jointObject instance and assign it to a given pointer
testlib.JointObjectPointer_initializeWithArray.argtypes = [ctypes.c_void_p(),
                                                           ctypes.c_int,
                                                           ctypes.c_int,
                                                           np.ctypeslib.ndpointer(dtype=ctypes.c_double)]
testlib.JointObjectPointer_initializeWithArray.restype = None

# // Given a void pointer to a jointObject instance, call a
# // setMappedMatrixData function that:
# // Sets data for already defined matrix object
testlib.JointObjectPointer_setMappedMatrixData.argtypes = [ctypes.c_void_p(),
                                                           ctypes.c_int,
                                                           ctypes.c_int,
                                                           np.ctypeslib.ndpointer(dtype=ctypes.c_double)]
testlib.JointObjectPointer_setMappedMatrixData.restype = None

# // Given a void pointer to a jointObject instance,
# // Obtain the dimensions of the Native array
testlib.JointObjectPointer_getNativeDimensions.argtypes = [ctypes.c_void_p(),
                                                           ctypes.POINTER(ctypes.c_int),
                                                           ctypes.POINTER(ctypes.c_int)]
testlib.JointObjectPointer_getNativeDimensions.restype = None

# // Given a void pointer to a jointObject instance,
# // Obtain the data of the Native array
testlib.JointObjectPointer_getNativeMatrixData.argtypes = [ctypes.c_void_p()]
testlib.JointObjectPointer_getNativeMatrixData.restype =\
    np.ctypeslib.ndpointer(dtype=ctypes.c_double, shape=(0, 0))


# // Given a void pointer to a jointObject instance, call a
# // modifyMappedMatrix function
testlib.JointObjectPointer_modifyMappedMatrix.argtypes = [ctypes.c_void_p(),
                                                          ctypes.c_int,
                                                          ctypes.c_int,
                                                          ctypes.c_double]
testlib.JointObjectPointer_modifyMappedMatrix.restype = None

# // Given a void pointer to a jointObject instance, call a
# // modifyNativeMatrix function
testlib.JointObjectPointer_modifyNativeMatrix.argtypes = [ctypes.c_void_p(),
                                                          ctypes.c_int,
                                                          ctypes.c_int,
                                                          ctypes.c_double]
testlib.JointObjectPointer_modifyNativeMatrix.restype = None

# // Given a void pointer to a jointObject instance, call a
# // print Native Matrix function
testlib.JointObjectPointer_printNativeMatrix.argtypes = [ctypes.c_void_p()]
testlib.JointObjectPointer_printNativeMatrix.restype = None

# // Given a void pointer to a jointObject instance, call a
# // print Mapped Matrix function
testlib.JointObjectPointer_printMappedMatrix.argtypes = [ctypes.c_void_p()]
testlib.JointObjectPointer_printMappedMatrix.restype = None

# //Destroy an jointObject pointer masked to by the vPointer
testlib.JointObjectPointer_deleteJointPointer.argtypes = argtypes = [ctypes.c_void_p()]
testlib.JointObjectPointer_deleteJointPointer.restype = None


class CPythonJointObject(object):
    """Test class for a c object accessed from python"""

    def __init__(self):
        self.lib = testlib
        self.jointObject = ctypes.c_void_p()
        self.mappedArray = None

    def jointObject_initializeWithArray(self, array):
        rows, cols = array.shape
        self.mappedArray = array
        self.lib.JointObjectPointer_initializeWithArray(ctypes.byref(self.jointObject),
                                                        rows,
                                                        cols,
                                                        array)

    def jointObject_setMappedMatrixData(self, array):
        rows, cols = array.shape
        self.mappedArray = array
        self.lib.JointObjectPointer_setMappedMatrixData(self.jointObject,
                                                        rows,
                                                        cols,
                                                        array)

    def jointObject_getNativeMatrixData(self):
        """Warning, this passes the Matrix to python by value not by reference,
        To pass by reference, use Mapper Matrix"""
        nRows = ctypes.c_int()
        nCols = ctypes.c_int()
        self.lib.JointObjectPointer_getNativeDimensions(self.jointObject,
                                                        ctypes.byref(nRows),
                                                        ctypes.byref(nCols))

        self.lib.JointObjectPointer_getNativeMatrixData.restype =\
            np.ctypeslib.ndpointer(dtype=ctypes.c_double, shape=(nRows.value, nCols.value))

        nativeArray = self.lib.JointObjectPointer_getNativeMatrixData(self.jointObject)
        return nativeArray

    def jointObject_modifyMappedMatrix(self, i, j, newValue):
        self.lib.JointObjectPointer_modifyMappedMatrix(self.jointObject,
                                                       i,
                                                       j,
                                                       newValue)

    def jointObject_modifyNativeMatrix(self, i, j, newValue):
        self.lib.JointObjectPointer_modifyNativeMatrix(self.jointObject,
                                                       i,
                                                       j,
                                                       newValue)

    def jointObject_printMappedMatrix(self):
        self.lib.JointObjectPointer_printMappedMatrix(self.jointObject)

    def jointObject_printNativeMatrix(self):
        self.lib.JointObjectPointer_printNativeMatrix(self.jointObject)

    def __del__(self):
        self.lib.JointObjectPointer_deleteJointPointer(self.jointObject)


if (__name__ == "__main__"):
    # Declare matrix
    n = 10
    m = 4
    testArray = np.arange(n * m, dtype="float64")
    testArray.shape = (n, m)
    print testArray
    squareArray(testArray)
    print testArray

    testJointObject = CPythonJointObject()
    testJointObject.jointObject_initializeWithArray(testArray)
    testJointObject.jointObject_printMappedMatrix()

    testJointObject.mappedArray[0, 0] = 0.1
    testJointObject.jointObject_printMappedMatrix()

    testJointObject.jointObject_modifyMappedMatrix(0, 1, 25)
    print testArray

    n = 4
    m = 5
    testArray2 = np.arange(n * m, dtype="float64")
    testArray2.shape = (n, m)
    testJointObject.jointObject_setMappedMatrixData(testArray2)
    print testArray2
    testJointObject.jointObject_printMappedMatrix()

    testJointObject.jointObject_printNativeMatrix()
    testJointObject.jointObject_modifyNativeMatrix(0, 1, 25)
    testJointObject.jointObject_printNativeMatrix()

    nativeArray = testJointObject.jointObject_getNativeMatrixData()
    print nativeArray
