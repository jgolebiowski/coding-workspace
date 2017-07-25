import graphAttack as ga
import numpy as np
import pickle
"""Control script"""


pickleFilename = "dataSet/notMNISTreformatted.pkl"
with open(pickleFilename, "rb") as fp:
    allDatasets = pickle.load(fp)

X = allDatasets["trainDataset"]
Y = allDatasets["trainLabels"]

with open("testData.pkl", "wb") as fp:
    dset = dict(X=X[0:10000], Y=Y[0:1000])
    pickle.dump(dset, fp)
    
Xtest = allDatasets["testDataset"]
Ytest = allDatasets["testLabels"]

Xvalid = allDatasets["validDataset"]
Yvalid = allDatasets["validLabels"]


for index in [0]:
    print(("Training with:", index))

    mainGraph = ga.Graph()
    ffeed = mainGraph.addOperation(ga.Variable(Xtest), doGradient=False, feederOperation=True)
    feedDrop = mainGraph.addOperation(ga.DropoutOperation(
        ffeed, 0.25), doGradient=False, finalOperation=False)

    l1 = ga.addDenseLayer(mainGraph, 800,
                          inputOperation=feedDrop,
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
        ga.CrossEntropyCostSoftmax(l2, Ytest),
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
                             initialLearningRate=1e-2,
                             momentumTerm=0.9,
                             function=fprime)

    params = adaGrad.minimize(1e3)
    mainGraph.attachParameters(params)
    print("train: Trained with:", index)
    print("train: Accuracy on train set:", ga.calculateAccuracy(mainGraph, X, Y))
    print("train: Accuracy on cv set:", ga.calculateAccuracy(mainGraph, Xvalid, Yvalid))
    print("train: Accuracy on test set:", ga.calculateAccuracy(mainGraph, Xtest, Ytest))
