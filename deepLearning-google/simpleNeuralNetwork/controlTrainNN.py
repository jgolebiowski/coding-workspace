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


sizes = np.array([X.shape[1], 800, Y.shape[1]])

for index in [0, 0.1]:
    print("Training with:", index)
    net = NeuralNetwork(sizes=sizes,
                        lambdaValue=index,
                        dropoutInput=0.25,
                        dropoutHidden=0.5,
                        activationHidden=ReluActivation,
                        activationFinal=SoftmaxActivation,
                        cost=CrossEntropyCostSoftmax)

    param0 = net.ravelParameters(net.weights, net.biases)

    adaGrad = adaptiveSGD(trainingData=X,
                          trainingLabels=Y,
                          param0=param0,
                          epochs=1e3,
                          miniBatchSize=200,
                          initialLearningRate=1e-2,
                          momentumTerm=0.9,
                          function=net.getCost)

    params = adaGrad.minimize(1e3)
    net.unravelParameters(params)
    pickleFileName = "nnSGD_" + str(index) + ".pkl"
    with open(pickleFileName, "wb") as fp:
        pickle.dump(net, fp)
    with open(pickleFileName, "rb") as fp:
        net = pickle.load(fp)
    print("train: Trained with:", index)
    print("train: Accuracy on train set:", net.calculateAccuracy(X, Y))
    print("train: Accuracy on cv set:", net.calculateAccuracy(Xvalid, Yvalid))
    print("train: Accuracy on test set:", net.calculateAccuracy(Xtest, Ytest))
