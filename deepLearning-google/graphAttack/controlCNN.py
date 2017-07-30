import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""


pickleFilename = "testDataTensor.pkl"
with open(pickleFilename, "rb") as fp:
    X, Y = pickle.load(fp)

X = X[0:1000]
Y = Y[0:1000]
inputTens = X[0:1]
outputTens = None
filterTensor = np.random.random((10, 10, X.shape[3], 2))

graph = tf.Graph()
with graph.as_default():
    con = tf.nn.conv2d(inputTens, filterTensor, [1, 1, 1, 1], "SAME")

with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    conVal = con.eval()

print(conVal)


# ------ Graph testing


mainGraph = ga.Graph()
feed = mainGraph.addOperation(ga.Variable(X), doGradient=False, feederOperation=True)
ffeed = mainGraph.addOperation(ga.Im2colOperation(feed))
print(ffeed.shape)

nOutputNodes = 10

# wtemp = ga.generateRandomVariable(shape=(nOutputNodes, 28, 28, 1), transpose=True)
# wotemp = mainGraph.addOperation(wtemp, doGradient=True)
# wo = mainGraph.addOperation(ga.Im2colOperation(wtemp))
# print(wo.shape)

w = ga.generateRandomVariable(shape=(nOutputNodes, ffeed.shape[1]), transpose=True)
wo = mainGraph.addOperation(w, doGradient=True)
print(wo.shape)

b = ga.generateRandomVariable(shape=nOutputNodes, transpose=False)

bo = mainGraph.addOperation(b, doGradient=True)

mmot = mainGraph.addOperation(ga.MatMatmulOperation(ffeed, wo),
                              doGradient=False,
                              finalOperation=False)

mmo1 = mainGraph.addOperation(ga.Col2imgOperation(mmot, (2, 5, 1)))
mmo = mainGraph.addOperation(ga.Im2colOperation(mmo1))

addo = mainGraph.addOperation(ga.AddOperation(mmo, bo),
                              doGradient=False,
                              finalOperation=False)

acto = mainGraph.addOperation(ga.SoftmaxActivation(addo),
                              doGradient=False,
                              finalOperation=False)


fcost = mainGraph.addOperation(
    ga.CrossEntropyCostSoftmax(acto, Y),
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
analCostGraph, analGradientGraph = fprime(params, X, Y)
print(sum(abs(numGrad)))
print(sum(abs(analGradientGraph - numGrad)), analCostGraph)
