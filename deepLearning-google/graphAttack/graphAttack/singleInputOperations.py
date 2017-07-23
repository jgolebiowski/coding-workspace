"""This where implementations of individual operations live"""

from .coreOperation import *
from .coreNode import broadcast_shape, reduce_shape
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


class SoftmaxOperation(SingleInputOperation):
    """Perform softmax on a given axis"""
    name = "SoftmaxOperation"

    def __init__(self, inputA=None, axis=1):
        super().__init__(inputA)
        self.axis = axis

    def perform(self, X, theta=1.0):
        """
        Compute the softmax of each element along an axis of X.

        Parameters
        ----------
        X: ND-Array. Probably should be floats.
        theta (optional): float parameter, used as a multiplier
            prior to exponentiation. Default = 1.0
        axis (optional): axis to compute values along. Default is the
            first non-singleton axis.

        Returns an array the same size as X. The result will sum to 1
        along the specified axis.
        """
        axis = self.axis
        # make X at least 2d
        y = np.atleast_2d(X)

        # find axis
        if axis is None:
            axis = next(j[0] for j in enumerate(y.shape) if j[1] > 1)

        # multiply y against the theta parameter,
        y = y * float(theta)

        # subtract the max for numerical stability
        y = y - np.expand_dims(np.max(y, axis=axis), axis)

        # exponentiate y
        y = np.exp(y)

        # take the sum along the specified axis
        ax_sum = np.expand_dims(np.sum(y, axis=axis), axis)

        # finally: divide elementwise
        p = y / ax_sum

        # flatten if X was 1D
        if len(X.shape) == 1:
            p = p.flatten()

        return p

    def performGradient(self, inputA=None):
        """Evaluate the gradient of softmax"""
        if (self.endNode):
            grad = np.ones(self.inputA.shape)
        else:
            grad = np.zeros(self.inputA.shape)
            for out in self.outputs:
                grad += out.getGradient(self)

        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n Value:\n", self.getValue())
        grad = (np.identity(self.shape[0]) - self.getValue()) * grad * self.getValue()
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\nGrad:\n", grad)
        return grad


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
