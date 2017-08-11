"""Additional utilities"""
import numpy as np

from ..coreDataContainers import Variable, TransposedVariable


def generateRandomVariable(shape, transpose=False):
    """Generate a ga.Variable of a given shape filled with random values
    from a Gaussian distribution with mean 0 and standard deviation 1
    If the transpose flag is set, generate a transposeVariable with the
    external shape given by shape

    Parameters
    ----------
    shape : tuple
        Shape of the desired variable
    transpose : bool
        If true, generate ga.Transposed variable with the shape being shape.T

    Returns
    -------
    ga.Variable
        generated random variable
    """

    if np.size(shape) == 1:
        reduction = 1
    else:
        reduction = np.sqrt(shape[0])
        # reduction = 1
        # for num in shape[1:]:
        #     reduction *= num
        # reduction = np.sqrt(reduction)

    X = np.random.random(shape) / reduction
    if (transpose):
        return TransposedVariable(X)
    else:
        return Variable(X)


def calculateAccuracy(graph, data, labels):
    """Feed data to a graph, ask it for predictions and obtain accuracy

    Parameters
    ----------
    graph : ga.Graph
        calculation graph
    data : np.array
        Input data
    labels : np.array
        labels for the data

    Returns
    -------
    float
        accuracy as a number from 0 to 1
    """
    graph.resetAll()
    graph.feederOperation.assignData(data)
    preds = graph.makePredictions()

    if np.size(labels.shape) == 1:
        nExamples = 1
    else:
        nExamples = labels.shape[0]

    error = np.sum(np.abs(preds - labels)) / (2 * nExamples)
    return 1 - error
