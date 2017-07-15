from mlModule.softmaxLogisticRegression import SoftmaxLinearRegression
from mlModule.adaptiveSGD import adaptiveSGD
from mlModule.neuralNetworks.neuralNetwork import *
from mlModule.neuralNetworks.neuralNetworkUtilities import *

import numpy as np



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

Xcheck2 = np.arange(1, 7).reshape((2, 3))
Ycheck2 = np.array([[1, 0], [0, 1]])

Xcheck = np.arange(1, 4).reshape((1, 3))
Ycheck = np.array([1, 0])

net = NeuralNetwork(sizes=sizes,
                    lambdaValue=1,
                    activationHidden=SigmoidActivation,
                    activationFinal=SigmoidActivation,
                    cost=CrossEntropyCostSigmoid)

# net.weights = [np.arange(1, 13).reshape(4, 3), np.arange(1, 9).reshape(2, 4)]
# net.biases = [np.arange(1, 5), np.arange(1, 3)]

params = net.ravelParameters(net.weights, net.biases)
analCost, analGrad = net.getCost(params, Xcheck2, Ycheck2)
numGrad = net.getNumericalGradient(params, Xcheck2, Ycheck2)

print np.sum(np.abs(analGrad - numGrad))