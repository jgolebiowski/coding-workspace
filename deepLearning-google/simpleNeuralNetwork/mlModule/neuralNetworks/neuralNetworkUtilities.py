
"""Module for different costs and activations"""
import numpy as np


class SigmoidActivation(object):
    """Simple class to implement a sigmoid activation function"""

    @staticmethod
    def val(z):
        """The sigmoid function."""
        return 1.0 / (1.0 + np.exp(-z))

    @staticmethod
    def prime(z):
        """Derivative of the sigmoid function."""
        return SigmoidActivation.val(z) * (1 - SigmoidActivation.val(z))


class ReluActivation(object):
    """Simple class to implement a ReLU activation function"""

    @staticmethod
    def val(z):
        """The ReLu function"""
        return np.maximum(z, 0)

    @staticmethod
    def prime(z):
        """The derevative of thr Relu function"""
        return ReluActivation.val(z) / z


class QuadraticCost(object):
    """Class for calculating cost
    parameters are te activation function on the last layer
    this is often needed to caluclate delta"""

    def __init__(self, activationFinal):
        self.activationFinal = activationFinal

    @staticmethod
    def val(a, y):
        """Return the cost associated with an output ``a`` and desired output
        ``y``.

        """
        return (0.5 / len(y)) * np.sum(np.sum(np.square(a - y), axis=1))

    def prime(self, a, y, z):
        """Return the error delta from the output layer.
        Given by te derevative of the cost with respect to
        the score
        """
        return (1.0 / len(y)) * (a - y) * self.activationFinal.prime(z)


class CrossEntropyCostSigmoid(object):
    """Class for calculating cost using cross-entropy,
    this is optimized to be used with a sigmoid activation function in the last layer,
    Will not work properly with a different activation function"""

    def __init__(self, activationFinal):
        if (activationFinal.__name__ != "SigmoidActivation"):
            raise ValueError("This cost works only with Sigmoid activation function")
        self.activationFinal = activationFinal

    @staticmethod
    def val(a, y):
        """Return the cost associated with an output ``a`` and desired output
        ``y``.  Note that np.nan_to_num is used to ensure numerical
        stability.  In particular, if both ``a`` and ``y`` have a 1.0
        in the same slot, then the expression (1-y)*np.log(1-a)
        returns nan.  The np.nan_to_num ensures that that is converted
        to the correct value (0.0).

        """
        return (1.0 / len(a)) * np.sum(np.nan_to_num(-y * np.log(a) - (1 - y) * np.log(1 - a)))

    def prime(self, a, y, z):
        """Return the error delta from the output layer.
        Given by te derevative of the cost with respect to
        the score
        """
        return (a - y)
