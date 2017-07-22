"""This where implementations of individual operations live"""

from .coreOperation import *
from .coreNode import broadcast_shape, reduce_shape
import numpy as np


class SumAllOperation(SingleInputOperation):
    '''Sum all elements together'''
    name = "SumAllOperation"

    def setShape(self):
        """Set the output shape"""
        self.shape = (1, )

    def perform(self, a):
        """Perform MatMul"""
        return np.sum(a)

    def performGradient(self, input=None):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self)

        return grad * np.ones(self.inputA.shape)


class SumSquaredOperation(SingleInputOperation):
    '''Sum all elements together'''
    name = "SumSquaresOperation"

    def setShape(self):
        """Set the output shape"""
        self.shape = (1, )

    def perform(self, a):
        """Perform MatMul"""
        return np.sum(np.square(a))

    def performGradient(self, input=None):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self)

        return grad * self.inputA.getValue() * 2
