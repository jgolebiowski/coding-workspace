from simpleLogisticRegression import SoftmaxLinearRegression
import cPickle as pickle
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


"""Control script"""

pickleFilename = "dataSet/notMNISTreformatted.pkl"
with open(pickleFilename, "rb") as fp:
    allDatasets = pickle.load(fp)

X = allDatasets["trainDataset"][0:30000]
Y = allDatasets["trainLabels"][0:30000]

Xtest = allDatasets["testDataset"]
Ytest = allDatasets["testLabels"]

logReg = SoftmaxLinearRegression(X, Y, 0.0001)
param0 = np.random.random(logReg.nClasses + logReg.nClasses * logReg.nFeatures)
print(logReg.getCost(param0, X, Y))

# res = scipy.optimize.minimize(logReg.getCost, param0, args=(X, Y), method="BFGS", jac=True)
# print res
# logReg.attachParameters(res.x)

# with open("logReg.pkl", "wb") as fp:
#     pickle.dump(logReg, fp)
with open("logReg.pkl", "rb") as fp:
    logReg = pickle.load(fp)

print("Accuracy on train set:", logReg.calculateAccuracy(X, Y))
print("Accuracy on test set:", logReg.calculateAccuracy(Xtest, Ytest))


def predictLetter(X, Y, index):
    labelsMap = np.array(["J", "D", "B", "F", "A", "G", "E", "I", "C", "H"])
    labels = logReg.makePredictions(X[index])
    print("The letter according to predictions: ", labelsMap[labels.argmax()])
    print("The letter according to label: ", labelsMap[Y[index].argmax()])

    fig = plt.figure()
    timer = fig.canvas.new_timer(interval = 2000)
    timer.add_callback(plt.close)

    plt.imshow(X[index].reshape(28, 28))
    timer.start()
    plt.show()
    plt.close()
