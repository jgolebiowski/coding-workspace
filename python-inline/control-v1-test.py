from scipy import weave
import numpy as np

def helloWorld(a):
	cCode = r"""std::cout << "Hello world! " << a << std::endl;"""
	varList = ["a"]
	weave.inline(cCode, varList)

def addition(A):
	length = len(A)
	cCode = r"""
	double sum = 0;
	for (int i = 0; i < length; i++)
	{
		sum = sum + A[i];
	}
	return_val = sum;
	"""

	varList = ["A", "length"]
	return weave.inline(cCode, varList)

def productArray(A):
	assert(type(A) == np.ndarray)
	length = len(A)
	
	supportCode = r"""
	double product(double a, double b)
	{
		return a*b;
	}
	"""

	cCode = r"""
	double prod = 1;
	for (int i = 0; i < length; i++)
	{
		prod = product(prod, A[i]);
	}
	return_val = prod;
	"""

	varList = ["A", "length"]
	return weave.inline(cCode, varList, 
						support_code = supportCode)

def additionList(A):
	cCode = r"""
	double sum = 0;
	length = A.length()
	for (int i = 0; i < length; i++)
	{
		sum = sum + A[i];
	}
	return_val = sum;
	"""

	varList = ["A"]
	return weave.inline(cCode, varList)

def binary_search(seq, t):
	min = 0
	max = len(seq) - 1 
	while True:
		if max < min: 
			return -1

		m=(min + max) /2 
		if seq[m] < t:
			min=m +1 
	
		elif seq[m] > t: 
			max=m -1
	
		else: 
			return m

def cBinarySearch(A, target):
	cCode = r"""
	int min = 0;
	int max = 
	"""