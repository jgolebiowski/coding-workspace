"""This where implementations of individual operations live"""

from .coreNode import *
import numpy as np


class Variable(Node):
    """Store some data ot feed in into the graph

    Attributes
    ----------
    gradA : np.array
        gradient with respect to inputA
    inputA : np.array
        data held by this variable, reference to self.result
    name : str
        Name of this operation
    result : np.array
        data held by this variable
    shape : tuple
        shape of ths output
    shapeExt : tuple
        Shape formatted to facilitate easy inspection from the outside
    """
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
        """Return a vaue of this Variable

        Returns
        -------
        np.array
            Data stored by the variable

        Raises
        ------
        AttributeError
            A value for the variable must be set
        """
        if (self.result is None):
            raise AttributeError("A value for the variable must be set")
        return self.result

    # def getValueExt(self):
    #     """Return a vaue of this Variable for use outside of the graph
    #     computations

    #     Returns
    #     -------
    #     np.array
    #         Data stored by the variable for external consumption

    #     Raises
    #     ------
    #     AttributeError
    #         A value for the variable must be set
    #     """
    #     if (self.result is None):
    #         raise AttributeError("A value for the variable must be set")
    #     return self.result

    def assignData(self, data, transpose=False):
        """Set the data being held by this operation

        Parameters
        ----------
        data : np.array
            Data to be held by the variable
        transpose : bool
            if true, hold the data transposed
        """
        if transpose:
            self.result = data.T
        else:
            self.result = data
        self.inputA = self.result
        self.setShape()

    def reset(self):
        """Reset the gradient of this variable"""
        self.gradA = None
        self.setShape()

    def getGradient(self, input=None):
        """Obtain gradient with respect to the input.
        parameter input added for consistancy

        Parameters
        ----------
        input : ga.Operation
            added for consistancy, this operation should have no inputs

        Returns
        -------
        np.array
            Gradient of the graphs final op with respect to the data in this varibale
        """

        if (self.gradA is None):
            self.gradA = self.performGradient()
        return self.gradA

    # def getGradientExt(self, input=None):
    #     """Obtain gradient with respect to the input for use outside
    #     of the graph computations. Routine added for consistancy
    #     parameter input added for consistancy

    #     Parameters
    #     ----------
    #     input : ga.Operation
    #         added for consistancy, this operation should have no inputs

    #     Returns
    #     -------
    #     np.array
    #         Gradient of the graphs final op with respect to the data in this varibale
    #         for external consumption
    #     """

    #     if (self.gradA is None):
    #         self.gradA = self.performGradient()
    #     return self.gradA

    def performGradient(self, input=None):
        """Find out the gradient"""
        grad = 0
        for out in self.outputs:
            grad += out.getGradient(self)
        return grad


# class TransposedVariable(Variable):
#     """This class is used make X * W.T easier by holding
#     a set of weights that can be accessed normally but are used
#     transposed in all of the computation

#     Attributes
#     ----------
#     gradA : np.array
#         gradient with respect to inputA
#     inputA : np.array
#         data held by this variable, reference to self.result
#     name : str
#         Name of this operation
#     result : np.array
#         data held by this variable
#     shape : tuple
#         shape of ths output
#     shapeExt : tuple
#         Shape formatted to facilitate easy inspection from the outside
#     """

#     name = "TransposedVariable"

#     def __init__(self, data):
#         super().__init__()

#         self.result = data.T
#         self.inputA = self.result
#         self.gradA = None
#         self.setShape()

#     def assignData(self, data, transpose=True):
#         """Set the data being held by this operation

#         Parameters
#         ----------
#         data : np.array
#             Data to be held by the variable
#         transpose : bool
#             if true, hold the data transposed
#         """
#         if transpose:
#             self.result = data.T
#         else:
#             self.result = data
#         self.inputA = self.result
#         self.setShape()

#     def setShape(self):
#         """Set the shape of the output of this Variable"""
#         self.shape = np.shape(self.result)
#         try:
#             self.shapeExt = np.shape(self.result.T)
#         except AttributeError:
#             pass

#     def getValueExt(self):
#         """Return a vaue of this Variable for use outside of the graph
#         computations

#         Returns
#         -------
#         np.array
#             Data stored by the variable for external consumption.
#             In this case the transpose of internally stored gradients

#         Raises
#         ------
#         AttributeError
#             A value for the variable must be set
#         """
#         if (self.result is None):
#             raise AttributeError("A value for the variable must be set")
#         return self.result.T

#     def getGradientExt(self, input=None):
#         """Obtain gradient with respect to the input for use outside
#         of the graph computations.

#         Parameters
#         ----------
#         input : ga.Operation
#             added for consistancy, this operation should have no inputs

#         Returns
#         -------
#         np.array
#             Gradient of the graphs final op with respect to the data in this varibale
#             for external consumption. In this case the transpose of internally stored gradients
#         """

#         if (self.gradA is None):
#             self.gradA = self.performGradient()
#         return self.gradA.T
