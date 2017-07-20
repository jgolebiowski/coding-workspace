"""This where implementations of individual operations live"""

from .coreOperation import *


class Variable(OneToOneOperation):
    """Multiply two inputs"""

    def __init__(self, data):
        self.inputA = None
        self.output = None

        self.result = data
        self.gradA = None

    def perform(self):
        """Return stored data, should not be called
        since the result is defined at initialization"""
        raise AttributeError("This should not be called since the result is defined at initialization")

    def assignData(self, data):
        """Set the data being held by this operation"""
        self.data = data

#TODO Make the variable a tensor and move some of the details to a tensor
# In this manner, operations will no longer be a basic object but an actual operation
