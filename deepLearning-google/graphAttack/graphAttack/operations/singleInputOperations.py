"""This where implementations of individual operations live"""

from ..coreOperation import *
from ..coreNode import broadcast_shape, reduce_shape
from .twoInputOperations import DivideOperation
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


class SumAxisOperation(SingleInputOperation):
    '''Sum all elements together along a given axis'''
    name = "SumAllOperation"

    def __init__(self, inputA=None, axis=0):
        self.axis = axis
        super().__init__(inputA)
        self.setShape()

    def setShape(self):
        """Set the output shape"""
        self.shape = np.delete(self.inputA.shape, self.axis)

    def perform(self, a):
        """Perform MatMul"""
        return np.sum(a, axis=self.axis)

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
        if (self.axis == 0):
            return (grad * np.ones(self.inputA.shape))
        elif (self.axis == 1):
            return (grad * np.ones(self.inputA.shape)).T
        else:
            raise NotImplemented("Must investigate this gradient further")


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


class ExpOperation(SingleInputOperation):
    '''Apply exponential function to all of the elements'''
    name = "ExpOperation"

    def setShape(self):
        """Set the output shape"""
        self.shape = self.inputA.shape

    def perform(self, a):
        """Perform Operation"""
        return np.exp(a)

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

        return grad * self.getValue()



# class ReducedExpOperation(SingleInputOperation):
#     '''Apply exponential function to all of the elements, reduced by the maximum'''
#     name = "ReducedExpOperation"

#     def __init__(self, inputA=None, axis=None):
#         super().__init__(inputA)
#         self.axis = axis
#         self.maxNum = np.expand_dims(np.max(inputA.getValue(), axis=axis), axis)
#         # np.finfo(inputA.)

#     def setShape(self):
#         """Set the output shape"""
#         self.shape = self.inputA.shape

#     def perform(self, a):
#         """Perform ReducedExp"""
#         print("ReducedExp:", np.exp(a - self.maxNum))
#         return np.exp(a - self.maxNum)

#     def performGradient(self, input=None):
#         """Find out the gradient with respect to the parameter
#         the key is:
#         inputA => 0
#         inputB => 1"""
#         if (self.endNode):
#             grad = np.ones(self.inputA.shape)
#         else:
#             grad = np.zeros(self.inputA.shape)
#             for out in self.outputs:
#                 grad += out.getGradient(self)

#         return grad * self.getValue()


# def softmaxOperation(inputA, axis=1):
#     """This is a softmax operation obtained by exponensing, summing and returning what is needed"""
#     a = DivideOperation(ReducedExpOperation(inputA, axis=axis),
#                         SumAxisOperation(ReducedExpOperation(inputA, axis=axis), axis))
#     a.name = "SoftmaxOperation"
#     return a
