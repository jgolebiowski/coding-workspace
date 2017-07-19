from mlModule.softmaxLogisticRegression import SoftmaxLinearRegression
from mlModule.adaptiveSGD import adaptiveSGD

import pickle as pickle
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

logReg = SoftmaxLinearRegression(X, Y, 0.0001)
param0 = np.random.random(logReg.nClasses + logReg.nClasses * logReg.nFeatures)

adaGrad = adaptiveSGD(trainingData=X,
                      trainingLabels=Y,
                      param0=param0,
                      epochs=1e4,
                      miniBatchSize=2000,
                      initialLearningRate=5e-3,
                      momentumTerm=0.9,
                      function=logReg.getCost)


params = adaGrad.minimize(1e3)
logReg.attachParameters(params)
with open("logRegSGD.pkl", "wb") as fp:
    pickle.dump(logReg, fp)
with open("logRegSGD.pkl", "rb") as fp:
    logReg = pickle.load(fp)

print("Accuracy on train set:", logReg.calculateAccuracy(X, Y))
print("Accuracy on cv set:", logReg.calculateAccuracy(Xvalid, Yvalid))
print("Accuracy on test set:", logReg.calculateAccuracy(Xtest, Ytest))


# res = scipy.optimize.minimize(logReg.getCost, param0, args=(X, Y), method="BFGS", jac=True)
# print res
# logReg.attachParameters(res.x)

# with open("logReg.pkl", "wb") as fp:
#     pickle.dump(logReg, fp)
# with open("logReg.pkl", "rb") as fp:
#     logReg = pickle.load(fp)

# print("Accuracy on train set:", logReg.calculateAccuracy(X, Y))
# print("Accuracy on test set:", logReg.calculateAccuracy(Xtest, Ytest))


# def predictLetter(X, Y, index):
#     labelsMap = np.array(["J", "D", "B", "F", "A", "G", "E", "I", "C", "H"])
#     labels = logReg.makePredictions(X[index])
#     print("The letter according to predictions: ", labelsMap[labels.argmax()])
#     print("The letter according to label: ", labelsMap[Y[index].argmax()])

#     fig = plt.figure()
#     timer = fig.canvas.new_timer(interval = 2000)
#     timer.add_callback(plt.close)

#     plt.imshow(X[index].reshape(28, 28))
#     timer.start()
#     plt.show()
#     plt.close()
