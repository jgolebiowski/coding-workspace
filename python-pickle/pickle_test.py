import numpy as np
import cPickle as pickle


class ExampleClass(object):
	"""Example class holding some functions and data"""

	def __init__(self, number1, number2):
		"""Initialization"""
		self.number1 = number1
		self.number2 = number2
		self.array = np.random.random((5, 5))

	def square(self, index=1):
		if (index == 1):
			self.number1 *= self.number1
		elif (index == 2):
			self.number2 *= self.number2
		else:
			print "Wrong index"

	def print_contents(self, array=True):
		print "Number1: {0}, Number2: {1}".format(self.number1, self.number2)
		if array is True:
			print "array:"
			print self.array


classInstance = ExampleClass(2, 4)
classInstance.print_contents(array=False)
classInstance.square(1)
classInstance.print_contents(array=False)
classInstance.square(2)
classInstance.print_contents()

#Open the file in write-binary (wb) mode
with open('filename.pkl', "wb") as fp:
	#Dump the object into the file
    pickle.dump(classInstance, fp)

#Open the file in read-binary format (rb)
with open('filename.pkl', "rb") as fp:
	#Load the contants of the file into python
    loadedClassInstance = pickle.load(fp)

print("Printing the contents of a loaded class")
loadedClassInstance.print_contents()
