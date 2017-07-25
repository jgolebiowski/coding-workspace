"""Additional utilities"""
import numpy as np

from ..coreDataContainers import Variable, TransposedVariable


def generateRandomVariable(shape, transpose=False):
    """Generate a ga.Variable of a given shape filled with random values
    from a Gaussian distribution with mean 0 and standard deviation 1
    If the transpose flag is set, generate a transposeVariable with the
    external shape given by shape"""

    X = np.random.random(shape)
    if (transpose):
        return TransposedVariable(X)
    else:
        return Variable(X)


def calculateAccuracy(graph, data, labels):
    """Feed data to a graph, ask it for predictions and obtain accuracy"""
    graph.resetAll()
    graph.feederOperation.assignData(data)
    preds = graph.makePredictions()

    if np.size(labels.shape) == 1:
        nExamples = 1
    else:
        nExamples = labels.shape[0]

    error = np.sum(np.abs(preds - labels)) / (2 * nExamples)
    return 1 - error
