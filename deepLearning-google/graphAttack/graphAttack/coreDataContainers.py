"""This where implementations of individual operations live"""

from .coreNode import *
import numpy as np


class Variable(Node):
    """Store some data ot feed in into the graph"""
    name = "Variable"

    def __init__(self, data):
        super().__init__()

        self.result = data
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

    def getValue(self):
        """Return a vaue of this Variable"""
        if (self.result is None):
            raise AttributeError("A value for the variable must be set")
        return self.result

    def assignData(self, data):
        """Set the data being held by this operation"""
        self.result = data
        self.setShape()

    def getGradient(self, input=None):
        """Obtain gradient with respect to the input.
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
