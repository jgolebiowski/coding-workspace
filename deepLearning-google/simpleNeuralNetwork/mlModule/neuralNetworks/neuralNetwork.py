"""neuralNetwork.py
~~~~~~~~~~~~~~

A module to implement the algorithm for a feedforward neural network.
Gradients are calculated using backpropagation.
Note that I have focused on making the code simple, easily readable, and
easily modifiable.  It is not optimized, and omits many desirable
features.

"""

import numpy as np
import scipy.optimize
from neuralNetworkUtilities import *


class NeuralNetwork(object):
    """The main class for my implementation of a neural network"""

    def __init__(self, sizes=None,
                 activationHidden=SigmoidActivation,
                 activationFinal=SigmoidActivation,
                 cost=QuadraticCost):

        self.nLayers = len(sizes)
        self.sizes = sizes

        self.activationHidden = activationHidden
        self.activationFinal = activationFinal
        self.cost = cost

        self.initializeWeights()

    def initializeWeights(self):
        """Initialize each weight using a Gaussian distribution with mean 0
        and standard deviation 1 over the square root of the number of
        weights connecting to the same neuron.  Initialize the biases
        using a Gaussian distribution with mean 0 and standard
        deviation 1."""

        self.weights = []
        self.biases = []
        self.totalParams = 0

        for lIndex in range(self.nLayers - 1):
            nInputNodes = self.sizes[lIndex]
            nOutputNodes = self.sizes[lIndex + 1]

            self.weights.append(np.random.random((nOutputNodes, nInputNodes)) / np.sqrt(nOutputNodes))
            self.biases.append(np.random.random((nOutputNodes)))
            self.totalParams += nOutputNodes + nOutputNodes * nInputNodes

    def feedforward(self, a):
        """Return the output of the network,
        given a matrix of features X

        Parameters
        ----------
        a : features for each example in a matrix form
            x.shape = (nExamples, nFeatures)
        """

        for lIndex in range(self.nLayers - 1):
            w = self.weights[lIndex]
            b = self.biases[lIndex]
            a = np.dot(a, w.T) + b[None, :]

            # If final layer, apply the final activation
            # Otherwise, apply the hidden one
            if (lIndex == self.nLayers - 2):
                a = self.activationFinal.val(a)
            else:
                a = self.activationHidden.val(a)
        return a

    def backPropagation(self, X, Y):
        """Feed forward to calculate cost
        later, use backpropagation to evlauate gradients
        of weights and biases"""

        gradB = [np.zeros(b.shape) for b in self.biases]
        gradW = [np.zeros(w.shape) for w in self.weights]
        cost = 0

        # Feed forward while storing activation values and scores
        a = X
        activations = [X]
        scores = [np.empty(0)]

        for lIndex in range(self.nLayers - 1):
            w = self.weights[lIndex]
            b = self.biases[lIndex]
            a = np.dot(a, w.T) + b[None, :]
            scores.append(a)

            # If final layer, apply the final activation
            # Otherwise, apply the hidden one
            if (lIndex == self.nLayers - 2):
                a = self.activationFinal.val(a)
                activations.append(a)
            else:
                a = self.activationHidden.val(a)
                activations.append(a)

        cost = self.cost.val(a, Y)

        return cost, gradW, gradB

    def getCost(self, params, X, Y):
        """Obtain cost and gradient given a vector of parameters and
        a dataset"""

        self.unravelParameters(params)
        cost, gradW, gradB = self.backPropagation(X, Y)

        return cost

    def getCostOnly(self, params, X, Y):
        """Obtain cost given a vector of parameters and
        a dataset"""

        self.unravelParameters(params)
        cost, gradW, gradB = self.backPropagation(X, Y)

        return cost

    def getNumericalGradient(self, params, X, Y, eps=1e-6):
        """Calculate numerical gradient given a parameters vector,
        see self.unravelParameters for more details on formatting"""

        numGrad = scipy.optimize.approx_fprime(params, self.getCostOnly, eps, X, Y)
        return numGrad

    def unravelParameters(self, params):
        """Unravel parameters from a vector to matrices and attach them

        Parameters
        ----------
        params : vector of parameters where for each layer
            param.shape = (nOutputNodes + nOutputNodes * nInputNodes)

            biases = param[0: nOutputNodes]
            weights = param[nOutputNodes:].reshape(nOutputNodes, nInputNodes)

            it can be composed as
            param[0: nOutputNodes] = biases
            param[nOutputNodes:] = weigthts.ravel()"""

        begPointer = 0
        for lIndex in range(self.nLayers - 1):
            nInputNodes = self.sizes[lIndex]
            nOutputNodes = self.sizes[lIndex + 1]

            self.biases[lIndex] = params[begPointer: begPointer + nOutputNodes]
            self.weights[lIndex] =\
                params[begPointer + nOutputNodes: begPointer + nOutputNodes + nInputNodes *
                       nOutputNodes].reshape(nOutputNodes, nInputNodes)

            begPointer += nOutputNodes + nOutputNodes * nInputNodes

    def ravelParameters(self, weights, biases):
        """ravel parameters from matrices to a vector

        Parameters
        ----------
        params : vector of parameters where for each layer
            param.shape = (nOutputNodes + nOutputNodes * nInputNodes)

            biases = param[0: nOutputNodes]
            weights = param[nOutputNodes:].reshape(nOutputNodes, nInputNodes)

            it can be composed as
            param[0: nOutputNodes] = biases
            param[nOutputNodes:] = weigthts.ravel()"""

        params = np.zeros(self.totalParams)
        begPointer = 0

        for lIndex in range(self.nLayers - 1):
            nInputNodes = self.sizes[lIndex]
            nOutputNodes = self.sizes[lIndex + 1]

            params[begPointer: begPointer + nOutputNodes] = biases[lIndex].ravel()
            params[begPointer + nOutputNodes: begPointer + nOutputNodes + nInputNodes * nOutputNodes] =\
                weights[lIndex].ravel()

            begPointer += nOutputNodes + nOutputNodes * nInputNodes

        return params