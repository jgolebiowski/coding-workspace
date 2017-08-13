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

maxPoolOP = ga.addConv2dLayer(mainGraph,
                  inputOperation=feed,
                  nFilters=2,
                  filterHeigth=9,
                  filterWidth=9,
                  padding="SAME",
                  convStride=1,
                  activation=ga.ReLUActivation,
                  pooling=ga.MaxPoolOperation,
                  poolHeight=4,
                  poolWidth=4,
                  poolStride=3)

flattenOp = mainGraph.addOperation(ga.Im2colOperation(maxPoolOP))
acto = mainGraph.addOperation(ga.SoftmaxActivation(flattenOp),
                              doGradient=False,
                              finalOperation=False)

Yt = np.random.random((2,162)) + 1e-4
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
