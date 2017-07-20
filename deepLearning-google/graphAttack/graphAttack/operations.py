"""This where implementations of individual operations live"""

from .coreOperation import *


class MultiplyOperation(TwoToOneOperation):
    """Multiply two inputs"""

    def perform(self, a, b):
        """Multiply two together"""
        return a * b

