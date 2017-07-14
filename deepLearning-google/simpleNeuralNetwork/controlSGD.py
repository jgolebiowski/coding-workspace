from mlModule.softmaxLogisticRegression import SoftmaxLinearRegression
from mlModule.adaptiveSGD import adaptiveSGD
import cPickle as pickle
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


"""Control script"""


X = np.arange(100)
Y = X * 2 + 1


def func(params, X, Y):
    """ax + b"""
    predictions = params[0] * X + params[1]
    costTemp = predictions - Y
    cost = (1.0 / (2.0 * len(X))) * np.dot(costTemp, costTemp)

    grad = np.zeros(2)
    grad[0] = (1.0 / len(X)) * np.dot(X, costTemp)
    grad[1] = (1.0 / len(X)) * np.sum(costTemp)

    return cost, grad

param0 = np.array([1, 0])
func(param0, X, Y)


adaGrad = adaptiveSGD(trainingData=X,
                      trainingLabels=Y,
                      param0=param0,
                      epochs=1e3,
                      miniBatchSize=20,
                      initialLearningRate=1e-1,
                      momentumTerm=0.9,
                      function=func)

params = adaGrad.minimize(1e1)
print params
print func(params, X, Y)[0]

res = scipy.optimize.minimize(func, param0, args=(X, Y), method="BFGS", jac=True)
print res
