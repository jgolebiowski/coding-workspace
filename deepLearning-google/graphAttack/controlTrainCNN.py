import graphAttack as ga
import numpy as np
import pickle
"""Control script"""


pickleFilename = "dataSet/notMNIST.pickle"
with open(pickleFilename, "rb") as fp:
    allDatasets = pickle.load(fp)

X = allDatasets["train_dataset"]
Y = allDatasets["train_labels"]

Xtest = allDatasets["test_dataset"]
Ytest = allDatasets["test_labels"]

Xvalid = allDatasets["valid_dataset"]
Yvalid = allDatasets["valid_labels"]

# pickleFilename = "testData.pkl"
# with open(pickleFilename, "rb") as fp:
#     allDatasets = pickle.load(fp)

# X = allDatasets["X"][0:1000]
# Y = allDatasets["Y"]


for index in [0]:
    print(("Training with:", index))

    mainGraph = ga.Graph()
    feed = mainGraph.addOperation(ga.Variable(X), doGradient=False, feederOperation=True)

    cnn1 = ga.addConv2dLayer(mainGraph,
                  inputOperation=feed,
                  nFilters=20,
                  filterHeigth=5,
                  filterWidth=5,
                  padding="SAME",
                  convStride=1,
                  activation=ga.ReLUActivation,
                  pooling=ga.MaxPoolOperation,
                  poolHeight=2,
                  poolWidth=2,
                  poolStride=2)


    l1 = ga.addDenseLayer(mainGraph, 500,
                          inputOperation=cnn1,
                          activation=ga.ReLUActivation,
                          dropoutRate=0.5,
                          w=None,
                          b=None)
    l2 = ga.addDenseLayer(mainGraph, 10,
                          inputOperation=l1,
                          activation=ga.SoftmaxActivation,
                          dropoutRate=0,
                          w=None,
                          b=None)
    fcost = mainGraph.addOperation(
        ga.CrossEntropyCostSoftmax(l2, Y),
        doGradient=False,
        finalOperation=True)

    def fprime(p, data, labels):
        mainGraph.feederOperation.assignData(data)
        mainGraph.costOperation.assignLabels(labels)
        mainGraph.attachParameters(p)
        mainGraph.resetAll()
        c = mainGraph.feedForward()
        mainGraph.feedBackward()
        g = mainGraph.unrollGradients()
        return c, g

    param0 = mainGraph.unrollGradientParameters()
    adaGrad = ga.adaptiveSGD(trainingData=X,
                             trainingLabels=Y,
                             param0=param0,
                             epochs=1e2,
                             miniBatchSize=200,
                             initialLearningRate=5e-3,
                             momentumTerm=0.9,
                             testFrequency=1e3,
                             function=fprime)

    params = adaGrad.minimize(True)
    mainGraph.attachParameters(params)

    pickleFileName = "graphSGD_" + str(index) + ".pkl"
    with open(pickleFileName, "wb") as fp:
        mainGraph.resetAll()
        pickle.dump(mainGraph, fp)
    with open(pickleFileName, "rb") as fp:
        mainGraph = pickle.load(fp)

    print("train: Trained with:", index)
    print("train: Accuracy on train set:", ga.calculateAccuracy(mainGraph, X, Y))
    print("train: Accuracy on cv set:", ga.calculateAccuracy(mainGraph, Xvalid, Yvalid))
    print("train: Accuracy on test set:", ga.calculateAccuracy(mainGraph, Xtest, Ytest))