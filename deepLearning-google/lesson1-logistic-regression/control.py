from simpleLogisticRegression import SoftmaxLinearRegression
import cPickle as pickle
import numpy as np
import scipy.optimize

"""Control script"""

pickleFilename = "dataSet/notMNISTreformatted.pkl"
with open(pickleFilename, "rb") as fp:
    allDatasets = pickle.load(fp)

X = allDatasets["testDataset"]
Y = allDatasets["testLabels"]

# X = np.array([[0, 1],
#               [2, 3],
#               [4, 12],
#               [6, 7]])

# Y = np.array([[1., 0., 0.],
#               [0., 1., 0.],
#               [0., 0., 1.],
#               [0., 1., 0.]])

logReg = SoftmaxLinearRegression(X, Y, 1)
param0 = np.random.random(logReg.nClasses + logReg.nClasses * logReg.nFeatures)
print(logReg.getCostOnly(param0))

# numGrad = logReg.getNumericalGradient(param0)
# _, analGrad = logReg.getCost(param0)

# for i in range(len(numGrad)):
#     print numGrad[i], analGrad[i]

res = scipy.optimize.minimize(logReg.getCost, param0, method="BFGS", jac=True)
print res

# print(Y)
w, b = logReg.unrollParameters(res.x)
# print(logReg.makePredictions(X, w, b))
print(logReg.calculateAccuracy(X, Y, w, b))
