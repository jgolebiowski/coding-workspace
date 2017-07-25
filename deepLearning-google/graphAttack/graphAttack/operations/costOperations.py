"""This where implementations of individual operations live"""

from ..coreOperation import *
from ..coreNode import broadcast_shape, reduce_shape
import numpy as np


class QuadratiCcostOperation(CostOperation):
    '''Evaliate the quadratic cost given the labels'''
    name = "QuadratiCcostOperation"

    def setShape(self):
        """Set the output shape"""
        self.shape = (1, )

    def perform(self, a, y):
        """Perform costOperation"""
        return (0.5 / self.nExamples) * np.sum(np.square(a - y))

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
        return grad * (1.0 / self.nExamples) * (self.inputA.getValue() - self.labels)


class CrossEntropyCostSoftmax(CostOperation):
    '''Evaliate the CrossEntropy cost given the labels, works with softmax activation ONLY'''
    name = "CrossEntropyCostSoftmax"

    def setShape(self):
        """Set the output shape"""
        self.shape = (1, )

    def perform(self, a, y):
        """Perform costOperation"""
        predLog = np.nan_to_num(-np.log(a))
        cEntropyMat = np.multiply(y, predLog)
        return (1.0 / self.nExamples) * np.sum(cEntropyMat)

    def performGradient(self, input=None):
        """Find out the gradient with respect to the parameter"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self)
        return grad * (1.0 / self.nExamples) * (-self.labels / self.inputA.getValue())


    # def perform(self, a):
    #     """Perform MatMul"""
    #     return np.sum(np.square(a))

    # def performGradient(self, input=None):
    #     """Find out the gradient with respect to the parameter
    #     the key is:
    #     inputA => 0
    #     inputB => 1"""
    #     if (self.endNode):
    #         grad = np.ones(self.inputA.shape)
    #     else:
    #         grad = np.zeros(self.inputA.shape)
    #         for out in self.outputs:
    #             grad += out.getGradient(self)

    #     return grad * self.inputA.getValue() * 2
