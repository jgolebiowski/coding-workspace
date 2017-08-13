import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""


pickleFilename = "testDataTensor.pkl"
with open(pickleFilename, "rb") as fp:
    X, Y = pickle.load(fp)

Xt = X[0:2]
Yt = Y[0:2]

# ------ conv2D operation testing
mainGraph = ga.Graph()
feed = mainGraph.addOperation(ga.Variable(Xt), doGradient=False, feederOperation=True)

filterW = np.random.random((2, 1, 9, 9))
filterOp = mainGraph.addOperation(ga.Variable(filterW), doGradient=True, feederOperation=False)
opConv2d = mainGraph.addOperation(ga.Conv2dOperation(feed, filterOp, stride=1, paddingMethod="SAME"))

filterB = np.random.random((1, 2, 1, 1))
biasOpp = mainGraph.addOperation(ga.Variable(filterB), doGradient=True, feederOperation=False)
addConv2d = mainGraph.addOperation(ga.AddOperation(opConv2d, biasOpp),
                                   doGradient=False, feederOperation=False)


flattenOp = mainGraph.addOperation(ga.Im2colOperation(addConv2d))
acto = mainGraph.addOperation(ga.SoftmaxActivation(flattenOp),
                              doGradient=False,
                              finalOperation=False)

Yt = np.random.random(1568) + 1e-4
fcost = mainGraph.addOperation(
    ga.CrossEntropyCostSoftmax(acto, Yt),
    doGradient=False,
    finalOperation=True)


print(mainGraph)
import scipy.optimize
params = mainGraph.unrollGradientParameters()


def f(x):
    mainGraph.attachParameters(x)
    return mainGraph.getValue()


def fprime(p, data, labels):
    mainGraph.feederOperation.assignData(data)
    mainGraph.costOperation.assignLabels(labels)
    mainGraph.attachParameters(p)
    mainGraph.resetAll()
    c = mainGraph.feedForward()
    mainGraph.feedBackward()
    g = mainGraph.unrollGradients()
    return c, g


numGrad = scipy.optimize.approx_fprime(params, f, 1e-6)
analCostGraph, analGradientGraph = fprime(params, Xt, Yt)
print(sum(abs(numGrad)))
print(sum(abs(analGradientGraph - numGrad)), analCostGraph)

print(analGradientGraph - numGrad)
