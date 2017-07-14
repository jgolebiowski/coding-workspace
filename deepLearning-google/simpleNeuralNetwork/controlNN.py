from mlModule.softmaxLogisticRegression import SoftmaxLinearRegression
from mlModule.adaptiveSGD import adaptiveSGD
from mlModule.neuralNetworks.neuralNetwork import *
from mlModule.neuralNetworks.neuralNetworkUtilities import *

import cPickle as pickle
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


"""Control script"""

# pickleFilename = "dataSet/notMNISTreformatted.pkl"
# with open(pickleFilename, "rb") as fp:
#     allDatasets = pickle.load(fp)

# X = allDatasets["trainDataset"]
# Y = allDatasets["trainLabels"]

# Xtest = allDatasets["testDataset"]
# Ytest = allDatasets["testLabels"]

# Xvalid = allDatasets["validDataset"]
# Yvalid = allDatasets["validLabels"]

sizes = np.array([3, 4, 2])
Xcheck = np.array([1, 2, 3])
Ycheck = np.array([3, 4])

Xcheck2 = np.arange(1, 7).reshape((2, 3))
Ycheck2 = np.array([[3, 4], [5, 6]])

net = NeuralNetwork(sizes=sizes,
                    activationHidden=SigmoidActivation,
                    activationFinal=SigmoidActivation,
                    cost=QuadraticCost)


from mlModule.neuralNetworks.neutalNetworkExamplev0 import Network
oldNet = Network(sizes)
# oldNet.weights = net.weights[:]
# oldNet.biases = net.biases[:]

params = net.ravelParameters(net.weights, net.biases)
print net.getCost(params, Xcheck, Ycheck)
print net.getNumericalGradient(params, Xcheck, Ycheck)
print oldNet.backprop(Xcheck, Ycheck)
