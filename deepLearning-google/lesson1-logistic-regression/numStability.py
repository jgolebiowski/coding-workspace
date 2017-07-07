"""Numerical stability"""
import numpy as np

largeVar = 1e9
miniVar = 1e-6

testVar = largeVar
for i in range(int(1e6)):
    testVar += miniVar
testVar -= largeVar

print "%.3f" % testVar
