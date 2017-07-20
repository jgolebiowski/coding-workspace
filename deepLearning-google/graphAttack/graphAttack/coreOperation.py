"""Operation definition"""
from .coreTensor import Tensor


class Operation(Tensor):
    """Class for storing all possible operations"""

    def __init__(self):
        self.shape = None

    def get_value(self, graph):
        """Obtain value of the oprtation"""
        raise NotImplementedError("This is not yet implemented")

    def perform(self, *args, **kwargs):
        """Return the value of the operation given inputs"""
        raise NotImplementedError("This is an abstract class")

    def op_grads(self, *args, **kwargs):
        """Return the derevative of this operation with respect to
        each input"""
        raise NotImplementedError("This is an abstract class")
