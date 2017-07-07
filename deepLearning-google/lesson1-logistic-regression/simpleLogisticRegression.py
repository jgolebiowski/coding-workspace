from __future__ import print_function
import numpy as np
from six.moves import cPickle as pickle
import scipy.optimize


"""Simple Linear regression for multiclass classifier"""


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    expMat = np.exp(x)
    return np.divide(expMat.T, np.sum(expMat, 1)).T


class SoftmaxLinearRegression(object):
    """Class that holds most of the funtionalities

    Parameters
    ----------
    trainDataset : features for each example in a matrix form
        x.shape = (nExamples, nFeatures)

    trainLabels : labels for each example in a matrix form and
        in a one-hot notation
    y.shape = (nExamples, nClasses)
    """

    def __init__(self,
                 trainDataset,
                 trainLabels,
                 lambdaValue=0):

        self.nExamples = trainDataset.shape[0]
        self.nFeatures = trainDataset.shape[1]
        self.nClasses = trainLabels.shape[1]

        self.trainDataset = trainDataset
        self.trainLabels = trainLabels

        self.lambdaValue = lambdaValue
        self.weigths = None
        self.bias = None

    def makePredictions(self, x, w, b):
        """Return predicions for each example

        Parameters
        ----------
        x : features for each example in a matrix form
            x.shape = (nExamples, nFeatures)

        w : matrix of weights
            w.shape = (nClasses, nFeatures)

        b: vector of biases
            b.shape = (nClasses, )
        """

        probMat = self.findPredictionMatrix(x, w, b)
        for i in range(probMat.shape[0]):
            indexMax = np.argmax(probMat[i])
            probMat[i][:] = 0
            probMat[i][indexMax] = 1

        return probMat

    def calculateAccuracy(self, x, y, w, b):
        """Calculate accuracy given the test set

        Parameters
        ----------
        x : features for each example in a matrix form
            x.shape = (nExamples, nFeatures)

        y : labels for each example in a matrix form and in a one-hot notation
            y.shape = (nExamples, nClasses)

        w : matrix of weights
            w.shape = (nClasses, nFeatures)

        b: vector of biases
            b.shape = (nClasses, )
        """

        predictionMat = self.makePredictions(x, w, b)
        error = np.sum(np.abs(predictionMat - y)) / (2 * x.shape[0])
        return 1 - error

    def findPredictionMatrix(self, x, w, b):
        """Compose a matrix of predictions

        Parameters
        ----------
        x : features for each example in a matrix form
            x.shape = (nExamples, nFeatures)

        w : matrix of weights
            w.shape = (nClasses, nFeatures)

        b: vector of biases
            b.shape = (nClasses, )
        """

        # Calculate the matrix of predicitions as X * Theta.T + B
        predMat = np.dot(x, w.T) + b[None, :]

        # Calculate the softmax for each column
        probMat = softmax(predMat)

        return probMat

    def calculateCost(self, x, y, w, b):
        """Calaulate cost given trainnig examples

        Parameters
        ----------
        x : features for each example in a matrix form
            x.shape = (nExamples, nFeatures)

        y : labels for each example in a matrix form and in a one-hot notation
            y.shape = (nExamples, nClasses)

        w : matrix of weights
            w.shape = (nClasses, nFeatures)

        b: vector of biases
            b.shape = (nClasses, )
        """
        predictions = self.findPredictionMatrix(x, w, b)

        # ------ apply cross entropy to get cost
        predLog = -np.log(predictions)
        cEntropyMat = np.multiply(y, predLog)
        cost = (1.0 / self.nExamples) * np.sum(cEntropyMat)

        # ------ Calculate gradient
        gradW = (-1.0 / self.nExamples) * (np.dot((y - predictions).T, x))
        gradB = (-1.0 / self.nExamples) * (np.dot((y - predictions).T, np.ones(x.shape[0])))

        # ------ Add regularization
        cost += np.sum(np.square(w)) * self.lambdaValue / 2
        gradW += w * self.lambdaValue

        return cost, gradW, gradB

    def unrollParameters(self, param):
        """Calculate matrixes from a params vector

        Parameters
        ----------
        param : vector of parameters where
            param.shape = (nClasses + nClasses * nFeatures)

            biases = param[0: nClasses]
            weights = param[nClasses:].reshape(nClasses, nFeatures)

            it can be composed as
            param[0: nClasses] = biases
            param[nClasses:] = weigthts.ravel()

        """

        biases = param[0: self.nClasses]
        weights = param[self.nClasses:].reshape(self.nClasses, self.nFeatures)

        return weights, biases

    def getCost(self, x):
        """Calculate cost given a parameters vector,
        see self.unrollParameters for more details on formatting"""

        weights, biases = self.unrollParameters(x)
        cost, gradW, gradB =\
            self.calculateCost(self.trainDataset, self.trainLabels, weights, biases)

        grad = np.hstack((gradB.ravel(), gradW.ravel()))
        return cost, grad

    def getCostOnly(self, x):
        """Obtain only the cost, without gradient,
        see getCost for more details"""

        return self.getCost(x)[0]

    def getNumericalGradient(self, x, eps=1e-6):
        """Calculate numerical gradient given a parameters vector,
        see self.unrollParameters for more details on formatting"""

        numGrad = scipy.optimize.approx_fprime(x, self.getCostOnly, eps)
        return numGrad
