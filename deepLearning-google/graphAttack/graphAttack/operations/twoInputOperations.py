"""This where implementations of individual operations live"""

from ..coreOperation import *
from ..coreNode import broadcast_shape, reduce_shape
import numpy as np


class MultiplyOperation(TwoInputOperation):
    """Multiply two inputs"""
    name = "MultiplyOperation"

    def perform(self, a, b):
        """Multiply two together"""
        return np.multiply(a, b)

    def performGradient(self, input):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            if (input == 0):
                grad = np.ones(self.inputA.shape)
            elif (input == 1):
                grad = np.ones(self.inputB.shape)
            else:
                raise ValueError
        else:
            if (input == 0):
                grad = np.zeros(self.inputA.shape)
            elif (input == 1):
                grad = np.zeros(self.inputB.shape)
            else:
                raise ValueError

            for out in self.outputs:
                grad += reduce_shape(out.getGradient(self), grad)

            if (input == 0):
                grad = grad * self.inputB.getValue()
            elif (input == 1):
                grad = grad * self.inputA.getValue()
        return grad


class DivideOperation(TwoInputOperation):
    """Divide two inputs"""
    name = "DivideOperation"

    def perform(self, a, b):
        """Multiply two together"""
        return np.divide(a, b)

    def performGradient(self, input):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            if (input == 0):
                grad = np.ones(self.inputA.shape)
            elif (input == 1):
                grad = np.ones(self.inputB.shape)
            else:
                raise ValueError
        else:
            if (input == 0):
                grad = np.zeros(self.inputA.shape)
            elif (input == 1):
                grad = np.zeros(self.inputB.shape)
            else:
                raise ValueError

            for out in self.outputs:
                grad += reduce_shape(out.getGradient(self), grad)

            if (input == 0):
                grad = np.divide(grad, self.inputB.getValue())
            elif (input == 1):
                grad = np.divide(grad, np.square(self.inputA.getValue()))
        return grad


class AddOperation(TwoInputOperation):
    """add two inputs"""
    name = "AddOperation"

    def perform(self, a, b):
        """add two together"""
        return np.add(a, b)

    def performGradient(self, input):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            if (input == 0):
                grad = np.ones(self.inputA.shape)
            elif (input == 1):
                grad = np.ones(self.inputB.shape)
            else:
                raise ValueError
        else:
            if (input == 0):
                grad = np.zeros(self.inputA.shape)
            elif (input == 1):
                grad = np.zeros(self.inputB.shape)
            else:
                raise ValueError

            for out in self.outputs:
                grad += reduce_shape(out.getGradient(self), grad)
        return grad


class MatMatmulOperation(TwoInputOperation):
    '''MatrixMultiplication for 2d matrices'''
    name = "MatMatmulOperation"

    def setShape(self):
        """Set the output shape"""
        if not (len(self.inputA.shape) == 2 == len(self.inputB.shape)):
            raise ValueError("This should be used on arrays of ndims == 2")

        self.shape = self.inputA.shape[0], self.inputB.shape[1]

    def perform(self, a, b):
        """Perform MatMul"""
        return np.matmul(a, b)

    def performGradient(self, input):
        """Find out the gradient with respect to the parameter
        the key is:
        inputA => 0
        inputB => 1"""
        if (self.endNode):
            grad = np.ones(self.shape)
        else:
            grad = np.zeros(self.shape)
            for out in self.outputs:
                grad += out.getGradient(self)

        if (input == 0):
            grad = np.matmul(grad, self.inputB.getValue().T)
        elif (input == 1):
            grad = np.matmul(self.inputA.getValue().T, grad)

        return grad
