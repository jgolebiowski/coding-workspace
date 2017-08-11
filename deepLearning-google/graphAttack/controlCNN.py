import graphAttack as ga
import numpy as np
import pickle
import tensorflow as tf
"""Control script"""


pickleFilename = "testDataTensor.pkl"
with open(pickleFilename, "rb") as fp:
    X, Y = pickle.load(fp)

Xtf = X[0:1000].reshape(1000, 28, 28, 1)
Y = Y[0:1000]
inputTenstf = Xtf[0:10]
outputTens = None
filterTensortf = np.random.random((9, 9, Xtf.shape[3], 2))


graph = tf.Graph()
with graph.as_default():
    con = tf.nn.conv2d(inputTenstf, filterTensortf, [1, 1, 1, 1], "SAME")

with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    conVal = con.eval()

print(conVal.shape)

# ------ Convolution 2d
x_shape = (2, 3, 4, 4)
w_shape = (3, 3, 4, 4)
x = np.linspace(-0.1, 0.5, num=np.prod(x_shape)).reshape(x_shape)
w = np.linspace(-0.2, 0.3, num=np.prod(w_shape)).reshape(w_shape)
b = np.linspace(-0.1, 0.2, num=3)


mainGraph = ga.Graph()
feed = mainGraph.addOperation(ga.Variable(x), doGradient=False, feederOperation=True)
filterOp = mainGraph.addOperation(ga.Variable(w), doGradient=True, feederOperation=False)
opConv2d = mainGraph.addOperation(ga.Conv2dOperation(feed, filterOp, stride=2, padding=1))
biasOpp = mainGraph.addOperation(ga.Variable(b[None, :, None, None]), doGradient=True, feederOperation=False)
addConv2d = mainGraph.addOperation(ga.AddOperation(opConv2d, biasOpp), doGradient=False, feederOperation=False) 


N, C, H, W = opConv2d.inputA.shape
NF, C, FH, FW = opConv2d.inputB.shape
_, _, oH, oW = opConv2d.shape


correct_out = np.array([[[[-0.08759809, -0.10987781],
                           [-0.18387192, -0.2109216 ]],
                          [[ 0.21027089,  0.21661097],
                           [ 0.22847626,  0.23004637]],
                          [[ 0.50813986,  0.54309974],
                           [ 0.64082444,  0.67101435]]],
                         [[[-0.98053589, -1.03143541],
                           [-1.19128892, -1.24695841]],
                          [[ 0.69108355,  0.66880383],
                           [ 0.59480972,  0.56776003]],
                          [[ 2.36270298,  2.36904306],
                           [ 2.38090835,  2.38247847]]]])

# ------ Im2col operation testing
# mainGraph = ga.Graph()
# feed = mainGraph.addOperation(ga.Variable(X), doGradient=False, feederOperation=True)
# ffeed = mainGraph.addOperation(ga.Im2colOperation(feed))

# nOutputNodes = 10
# w = ga.generateRandomVariable(shape=(nOutputNodes, ffeed.shape[1]), transpose=True)
# wo = mainGraph.addOperation(w, doGradient=True)

# b = ga.generateRandomVariable(shape=nOutputNodes, transpose=False)
# bo = mainGraph.addOperation(b, doGradient=True)

# mmot = mainGraph.addOperation(ga.MatMatmulOperation(ffeed, wo),
#                               doGradient=False,
#                               finalOperation=False)

# mmo1 = mainGraph.addOperation(ga.Col2imgOperation(mmot, (2, 5, 1)))
# mmo = mainGraph.addOperation(ga.Im2colOperation(mmo1))

# addo = mainGraph.addOperation(ga.AddOperation(mmo, bo),
#                               doGradient=False,
#                               finalOperation=False)

# acto = mainGraph.addOperation(ga.SoftmaxActivation(addo),
#                               doGradient=False,
#                               finalOperation=False)


# fcost = mainGraph.addOperation(
#     ga.CrossEntropyCostSoftmax(acto, Y),
#     doGradient=False,
#     finalOperation=True)


# print(mainGraph)
# import scipy.optimize
# params = mainGraph.unrollGradientParameters()


# def f(x):
#     mainGraph.attachParameters(x)
#     return mainGraph.getValue()


# def fprime(p, data, labels):
#     mainGraph.feederOperation.assignData(data)
#     mainGraph.costOperation.assignLabels(labels)
#     mainGraph.attachParameters(p)
#     mainGraph.resetAll()
#     c = mainGraph.feedForward()
#     mainGraph.feedBackward()
#     g = mainGraph.unrollGradients()
#     return c, g


# numGrad = scipy.optimize.approx_fprime(params, f, 1e-6)
# analCostGraph, analGradientGraph = fprime(params, X, Y)
# print(sum(abs(numGrad)))
# print(sum(abs(analGradientGraph - numGrad)), analCostGraph)
