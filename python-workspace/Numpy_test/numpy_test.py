#!/usr/bin/python

import numpy as np


#######################
## Functions
#######################

class Number:
        """My class documentation string"""
        
        def __init__(self,n):
                self.value=n    
        def hello(self):
                """Print out an introductory sentenc"""
                print 'Hello my class! The value is:',self.value
        def add(self,n):
                """Increases the value by a certian amount"""
                self.value=self.value+n






#######################
## Main
#######################
print ''

test_array = np.empty( (1,2), dtype=object)
test_array[0,0] = Number(10)
print 'Whole test array'
print test_array
print '(0,0).value from test array'
print(test_array[0,0].value)

temp_array = np.empty( (2), dtype=object)
print 'temp array'
print temp_array

test_array = np.vstack( (test_array, temp_array) )
print 'Result of vstacking test and temp arrays'
print test_array

print ''
test_array[0,0].add(5)
print 'using a class functions for a class object stored in test array (0,0)'
print(test_array[0,0].value)

test_array[0,1] = Number(5)

test2 = np.array( [[1, 2], [3, 4], [5, 6]])
print 'print test2'
print test2 

print 'test2 shape'
print test2.shape

test3 = np.zeros( (2,2) )
print 'test3 = shape of test3'
print test3

test2 = np.vstack((test2, test3))
print 'vstacking test2 and test3'
print test2


