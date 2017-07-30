"""This where implementations of individual operations live"""

from ..coreOperation import *
from ..coreNode import broadcast_shape, reduce_shape
import numpy as np


class Im2colOperation(SingleInputOperation):
    '''Flatten the axis greater than 0 to turn
    dim > 2 tensors into 2d arrays'''
    name = "im2colOperation"

    def setShape(self):
        """Set the output shape"""
        inpShapeSize = len(self.inputA.shape)
        if (inpShapeSize >= 2):
            self.nExamples = self.inputA.shape[0]
            numFeatures = 1
            for index in range(inpShapeSize - 1):
                numFeatures *= self.inputA.shape[index + 1]
            self.shape = (self.nExamples, numFeatures)
        else:
            self.nExamples = 1
            self.shape = (self.nExamples, self.inputA.shape[0])

    def perform(self, a):
        """Perform the flattening"""
        return a.reshape(self.shape)

    def performGradient(self, input=None):
        """Find out the gradient with respect to the parameter"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self).reshape(self.inputA.shape)

        return grad


class Col2imgOperation(SingleInputOperation):
    '''Transform a 2d array into a multidimensional array'''
    name = "Col2imgOperation"

    def __init__(self, inputA=None, exampleShape=0):
        self.exampleShape = exampleShape
        super().__init__(inputA)
        self.setShape()

    def setShape(self):
        """Set the output shape"""
        inpShapeSize = len(self.inputA.shape)
        if (inpShapeSize >= 2):
            self.nExamples = self.inputA.shape[0]
            self.shape = (self.nExamples, ) + self.exampleShape
        else:
            self.nExamples = 1
            self.shape = (self.nExamples, ) + self.exampleShape

    def perform(self, a):
        """Perform the flattening"""
        return a.reshape(self.shape)

    def performGradient(self, input=None):
        """Find out the gradient with respect to the parameter"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self).reshape(self.inputA.shape)

        return grad
