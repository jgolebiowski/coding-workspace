"""Operation definition"""
from .coreNode import Node
from .coreNode import broadcast_shape
import numpy as np


class Operation(Node):
    """Class for storing all possible operations"""
    name = "Operation"

    def __init__(self):
        super().__init__()
        self.result = None

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "<%s>" % self.name
        return output

    def getValue(self, *args, **kwargs):
        """Obtain value of the oprtation"""
        raise NotImplementedError("This is not yet implemented")

    def getValueExt(self, *args, **kwargs):
        """Return a vaue of this Variable for use outside of the graph
        computations"""
        return self.getValue(*args, **kwargs)

    def perform(self, *args, **kwargs):
        """Return the value of the operation given inputs"""
        raise NotImplementedError("This is an abstract class, this routine should be implemented in children")

    def reset(self, *args, **kwargs):
        """Reset the values and gradients held by this operation"""
        raise NotImplementedError("This is an abstract class, this routine should be implemented in children")

    def getGradient(self, *args, **kwargs):
        """Return the derevative of this operation with respect to
        each input"""
        raise NotImplementedError("This is an abstract class, this routine should be implemented in children")

    def getGradientExt(self, *args, **kwargs):
        """Obtain gradient with respect to the input for use outside
        of the graph computations.
        parameter input added for consistancy"""
        return self.getGradient(*args, **kwargs)


class TwoInputOperation(Operation):
    """Operation accepting two input and returning one output"""
    name = "TwoInputOperation"

    def __init__(self, inputA=None, inputB=None):
        super().__init__()
        self.inputA = inputA
        self.inputB = inputB

        self.gradA = None
        self.gradB = None

        inputA.addOutput(self)
        inputB.addOutput(self)

        self.setShape()

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "<%s with inputs: (%s, %s) and outputs: (" % (self.name, self.inputA.name, self.inputB.name)
        for op in self.outputs:
            output += "%s, " % op.name
        output += ")>"
        return output

    def setShape(self):
        """Set the output shape"""
        self.shape = broadcast_shape(np.shape(self.inputA), np.shape(self.inputB))

    def reset(self):
        """Reset the values and gradients held by this operation"""
        self.result = None
        self.gradA = None
        self.gradB = None
        self.setShape()

    def getValue(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            self.result = self.perform(self.inputA.getValue(), self.inputB.getValue())
        return self.result

    def getGradient(self, input):
        """Obtain gradient with respect ot a chosen input"""
        if (input is self.inputA):
            if (self.gradA is None):
                self.gradA = self.performGradient(input=0)
            return self.gradA
        elif (input is self.inputB):
            if (self.gradB is None):
                self.gradB = self.performGradient(input=1)
            return self.gradB
        else:
            raise ValueError("Must select either gradient from inputA or inputB")


class SingleInputOperation(Operation):
    """Operation accepting one input and returning one output"""
    name = "OneInputOperation"

    def __init__(self, inputA=None):
        super().__init__()
        self.inputA = inputA

        self.gradA = None

        inputA.addOutput(self)

        self.setShape()

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "<%s with input: (%s) and outputs: (" % (self.name, self.inputA.name)
        for op in self.outputs:
            output += "%s, " % op.name
        output += ")>"
        return output

    def setShape(self):
        """Set the output shape"""
        self.shape = np.shape(self.inputA)

    def reset(self):
        """Reset the values and gradients held by this operation"""
        self.result = None
        self.gradA = None
        self.setShape()

    def getValue(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            self.result = self.perform(self.inputA.getValue())
        return self.result

    def getGradient(self, input=None):
        """Obtain gradient with respect to the input.
        parameter input added for consistancy"""

        if (input is self.inputA):
            if (self.gradA is None):
                self.gradA = self.performGradient()
            return self.gradA
        else:
            raise ValueError("Must select gradient from inputA")


class CostOperation(SingleInputOperation):
    """Operation accepting one input and one label, returning the cost
    Labels are to be provided as a standard numpy array, not an operation."""
    name = "CostOperation"

    def __init__(self, inputA, labels):
        super().__init__(inputA)
        self.labels = labels
        self.setShape()

        if (np.ndim(labels) >= 2):
            self.nExamples = labels.shape[0]
        else:
            self.nExamples = 1

    def setShape(self):
        """Set the output shape"""
        self.shape = (1, )

    def reset(self):
        """Reset the values and gradients held by this operation"""
        self.result = None
        self.gradA = None
        self.setShape()

    def assignLabels(self, labels):
        """Assign a new set of labels"""
        self.labels = labels
        if (np.ndim(labels) >= 2):
            self.nExamples = labels.shape[0]
        else:
            self.nExamples = 1

    def getValue(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            self.result = self.perform(self.inputA.getValue(), self.labels)
        return self.result

    def makePredictions(self):
        """Do not evaluate the cost but instead make predictions besed on input"""
        shape = self.inputA.getValue().shape
        predictions = np.zeros(shape)

        if np.size(shape) == 1:
            indexMax = np.argmax(self.inputA.getValue())
            predictions[indexMax] = 1
        else:
            for i, example in enumerate(self.inputA.getValue()):
                indexMax = np.unravel_index(example.argmax(), example.shape)
                predictions[i, indexMax] = 1

        return predictions
