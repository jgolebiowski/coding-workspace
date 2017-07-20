"""Operation definition"""
from .coreTensor import Tensor


class Operation(Tensor):
    """Class for storing all possible operations"""

    def __init__(self):
        self.shape = None

    def get_value(self, *args, **kwargs):
        """Obtain value of the oprtation"""
        raise NotImplementedError("This is not yet implemented")

    def perform(self, *args, **kwargs):
        """Return the value of the operation given inputs"""
        raise NotImplementedError("This is an abstract class")

    def reset(self, *args, **kwargs):
        """Reset the values and gradients held by this operation"""
        raise NotImplementedError("This is an abstract class")

    def op_grads(self, *args, **kwargs):
        """Return the derevative of this operation with respect to
        each input"""
        raise NotImplementedError("This is an abstract class")


class TwoToOneOperation(Operation):
    """Operation accepting two input and returning one output"""

    def __init__(self, inputA, inputB):
        self.inputA = inputA
        self.inputB = inputB
        self.output = None

        self.result = None
        self.gradA = None
        self.gradB = None

    def reset(self):
        """Reset the values and gradients held by this operation"""
        self.result = None
        self.gradA = None
        self.gradB = None

    def get_value(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            self.result = self.perform(self.inputA.get_value(), self.inputB.get_value())
        return self.result


class OneToOneOperation(Operation):
    """Operation accepting one input and returning one output"""

    def __init__(self, inputA):
        self.inputA = inputA
        self.output = None

        self.result = None
        self.gradA = None

    def reset(self):
        """Reset the values and gradients held by this operation"""
        self.result = None
        self.gradA = None

    def get_value(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            self.result = self.perform(self.inputA.get_value())
        return self.result

