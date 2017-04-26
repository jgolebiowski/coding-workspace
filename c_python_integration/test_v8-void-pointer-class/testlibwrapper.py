import numpy as np
import ctypes

#Load a ahsred library under that address
from os import getcwd


MYDIR = getcwd()
testTestLib = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")
#Test the library
testTestLib.hello_world()






class cAtoms(object):
	"""Test class"""
	def __init__(self):
		MYDIR = getcwd()
		self.testlib = ctypes.cdll.LoadLibrary(MYDIR+"/testlib.so")
		self.atomsObject = ctypes.c_void_p()

		#Define function parameters
		self.testlib.initialize_Atoms_void_pointer_from_array.argtypes = [ctypes.c_void_p(),
							np.ctypeslib.ndpointer(dtype=ctypes.c_double), 
                        	ctypes.c_int]
		self.testlib.initialize_Atoms_void_pointer_from_array.restype = None


	def initialize_atoms(self):
	    self.testlib.initialize_Atoms_void_pointer(ctypes.byref(self.atomsObject) )

	def initialize_from_array(self, array):
		 rows, cols = array.shape
		 self.testlib.initialize_Atoms_void_pointer_from_array(ctypes.byref(self.atomsObject),
		 														array,
		 														rows)

	def print_atoms(self):
		self.testlib.print_Atoms_pointer_positions(self.atomsObject )

	def __del__(self):
	    self.testlib.destroy_Atoms_void_pointer(self.atomsObject )

testAtoms = cAtoms()
testArray = np.ones((10,3))
testAtoms.initialize_from_array(testArray)
testAtoms.print_atoms()

testArray[0, 0] = 0
testAtoms.print_atoms()
