from mlModule.softmaxLogisticRegression import SoftmaxLinearRegression
from mlModule.adaptiveSGD import adaptiveSGD
from mlModule.neuralNetworks.neuralNetwork import *
from mlModule.neuralNetworks.neuralNetworkUtilities import *


import cPickle as pickle
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


"""Control script"""


pickleFilename = "dataSet/notMNISTreformatted.pkl"
with open(pickleFilename, "rb") as fp:
    allDatasets = pickle.load(fp)

X = allDatasets["trainDataset"]
Y = allDatasets["trainLabels"]

Xtest = allDatasets["testDataset"]
Ytest = allDatasets["testLabels"]

Xvalid = allDatasets["validDataset"]
Yvalid = allDatasets["validLabels"]


sizes = np.array([X.shape[1], 20, Y.shape[1]])

net = NeuralNetwork(sizes=sizes,
                    lambdaValue=1,
                    activationHidden=SigmoidActivation,
                    activationFinal=SigmoidActivation,
                    cost=CrossEntropyCostSigmoid)

param0 = net.ravelParameters(net.weights, net.biases)

adaGrad = adaptiveSGD(trainingData=X,
                      trainingLabels=Y,
                      param0=param0,
                      epochs=1e2,
                      miniBatchSize=1000,
                      initialLearningRate=1e-2,
                      momentumTerm=0.9,
                      function=net.getCost)


# params = adaGrad.minimize(adaGrad.epochs)
# net.unravelParameters(params)
# with open("nnSGD.pkl", "wb") as fp:
#     pickle.dump(net, fp)
with open("nnSGD.pkl", "rb") as fp:
    net = pickle.load(fp)

print("Accuracy on train set:", net.calculateAccuracy(X, Y))
print("Accuracy on cv set:", net.calculateAccuracy(Xvalid, Yvalid))
print("Accuracy on test set:", net.calculateAccuracy(Xtest, Ytest))
