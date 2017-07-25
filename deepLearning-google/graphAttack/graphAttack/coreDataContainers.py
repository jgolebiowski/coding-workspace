"""This where implementations of individual operations live"""

from .coreNode import *
import numpy as np


class Variable(Node):
    """Store some data ot feed in into the graph"""
    name = "Variable"

    def __init__(self, data=None):
        super().__init__()

        self.result = data
        self.inputA = self.result
        self.gradA = None
        self.setShape()

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "<%s with outputs: (" % (self.name)
        for op in self.outputs:
            output += "%s, " % op.name
        output += ")>"
        return output

    def setShape(self):
        """Set the shape of the output of this Variable"""
        self.shape = np.shape(self.result)
        self.shapeExt = self.shape

    def getValue(self):
        """Return a vaue of this Variable"""
        if (self.result is None):
            raise AttributeError("A value for the variable must be set")
        return self.result

    def getValueExt(self):
        """Return a vaue of this Variable for use outside of the graph
        computations"""
        if (self.result is None):
            raise AttributeError("A value for the variable must be set")
        return self.result

    def assignData(self, data, transpose=False):
        """Set the data being held by this operation"""
        if transpose:
            self.result = data.T
        else:
            self.result = data
        self.setShape()

    def reset(self):
        """Reset the gradient of this variable"""
        self.gradA = None
        self.setShape()

    def getGradient(self, input=None):
        """Obtain gradient with respect to the input.
        parameter input added for consistancy"""

        if (self.gradA is None):
            self.gradA = self.performGradient()
        return self.gradA

    def getGradientExt(self, input=None):
        """Obtain gradient with respect to the input for use outside
        of the graph computations.
        parameter input added for consistancy"""

        if (self.gradA is None):
            self.gradA = self.performGradient()
        return self.gradA

    def performGradient(self, input=None):
        """Find out the gradient"""
        grad = 0
        for out in self.outputs:
            grad += out.getGradient(self)
        return grad


class TransposedVariable(Variable):
    """This class is used make X * W.T easier by holding
    a set of weights that can be accessed normally but are used
    transposed in all of the computation"""

    name = "TransposedVariable"

    def __init__(self, data):
        super().__init__()

        self.result = data.T
        self.inputA = self.result
        self.gradA = None
        self.setShape()

    def assignData(self, data, transpose=True):
        """Set the data being held by this operation"""
        if transpose:
            self.result = data.T
        else:
            self.result = data
        self.setShape()

    def setShape(self):
        """Set the shape of the output of this Variable"""
        self.shape = np.shape(self.result)
        try:
            self.shapeExt = np.shape(self.result.T)
        except AttributeError:
            pass

    def getValueExt(self):
        """Return a vaue of this Variable for use outside of the graph
        computations"""
        if (self.result is None):
            raise AttributeError("A value for the variable must be set")
        return self.result.T

    def getGradientExt(self, input=None):
        """Obtain gradient with respect to the input for use outside
        of the graph computations.
        parameter input added for consistancy"""

        if (self.gradA is None):
            self.gradA = self.performGradient()
        return self.gradA.T
