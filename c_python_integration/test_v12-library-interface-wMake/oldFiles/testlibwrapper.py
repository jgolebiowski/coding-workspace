import numpy as np
import ctypes

#Load a ahsred library under that address
from os import getcwd


MYDIR = getcwd()
testlib = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")
#Test the library
testlib.hello_world()

#Define function parameters
testlib.initialize_Atoms_with_positions.argtypes = [ctypes.c_void_p(),
										np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                      					ctypes.c_int]
testlib.initialize_Atoms_with_positions.restype = None

testlib.set_Atoms_pointer_positions.argtypes = [ctypes.c_void_p(),
								np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                      			ctypes.c_int]
testlib.set_Atoms_pointer_positions.restype = None

testlib.modify_Atoms_pointer_positions.argtypes = [ctypes.c_void_p(),
                      					ctypes.c_int,
                      					ctypes.c_int,
                      					ctypes.c_double]
testlib.modify_Atoms_pointer_positions.restype = None


class cAtoms(object):
	"""Test class"""
	def __init__(self):
		MYDIR = getcwd()
		self.lib = testlib
		self.atomsObject = ctypes.c_void_p()




	def initialize_atoms(self):
	    self.lib.initialize_Atoms_void_pointer(ctypes.byref(self.atomsObject) )

	def initialize_with_positions(self, array):
		 rows, cols = array.shape
		 self.lib.initialize_Atoms_with_positions(ctypes.byref(self.atomsObject),
		 														array,
		 														rows)

	def set_positions(self, array):
		 rows, cols = array.shape
		 self.lib.set_Atoms_pointer_positions(self.atomsObject,
		 										array,
		 										rows)


	def modify_position(self, atomNumber, dimNumber, newPosition):
		self.lib.modify_Atoms_pointer_positions(self.atomsObject,
												atomNumber,
												dimNumber,
												newPosition)

	def print_atoms(self):
		self.lib.print_Atoms_pointer_positions(self.atomsObject )

	def __del__(self):
	    self.lib.destroy_Atoms_void_pointer(self.atomsObject )

testAtoms = cAtoms()
testArray = np.ones((5,3), dtype="float64")
testAtoms.initialize_with_positions(testArray)
testAtoms.print_atoms()

testArray[0, 0] = 0.1
testAtoms.print_atoms()

testAtoms.modify_position(3, 2, 10.7)
testAtoms.print_atoms()

print(testArray)

testArray2 = np.zeros((10, 3), dtype="float64")
testAtoms.set_positions(testArray2)
testAtoms.print_atoms()
