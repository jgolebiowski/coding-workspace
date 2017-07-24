import graphAttack as ga
import numpy as np


"""Control script"""

mainGraph = ga.Graph()

data1a = 10
data1b = 2

data2a = np.arange(3)
data2b = 7

# f0 = mainGraph.addOperation(ga.Variable(data1a), doGradient=True)
# f1 = mainGraph.addOperation(ga.Variable(data1b), doGradient=True)
# f2 = mainGraph.addOperation(ga.Variable(data2a), doGradient=True)
# f3 = mainGraph.addOperation(ga.Variable(data2b), doGradient=True)

# f4 = mainGraph.addOperation(
#     ga.MultiplyOperation(f0, f1),
#     doGradient=False,
#     finalOperation=False)
# f5 = mainGraph.addOperation(
#     ga.MultiplyOperation(f2, f3),
#     doGradient=False,
#     finalOperation=False)
# f6 = mainGraph.addOperation(
#     ga.AddOperation(f4, f5),
#     doGradient=False,
#     finalOperation=True)

# mainGraph.printGraph()
# print(mainGraph.feedForward())
# print(mainGraph.feedBackward())


X = np.array([[1.7, 0.2, 3],
              [0.5, 1.4, 1.2],
              [2.3, 1.1, 2.2]], dtype=float)

# labels = np.array([[0, 0, 1],
#                    [1, 0, 0],
#                    [0, 1, 0]], dtype=float)

labels = np.array([1, 0, 1])

W1 = np.array([[2, 0.2, 1.1],
               [0.3, 1, 4]])
B1 = np.array([1, 2])

W2 = np.array([[1.1, 3],
               [2, 3],
               [1, 1]])
B2 = np.array([1, 2, 3])

test = np.array([1, 3, 5])

ftest = mainGraph.addOperation(ga.Variable(test), doGradient=False)

f0 = mainGraph.addOperation(ga.Variable(X), doGradient=False)
f1 = mainGraph.addOperation(ga.TransposedVariable(W1), doGradient=True)
f2 = mainGraph.addOperation(ga.Variable(B1), doGradient=True)
f3 = mainGraph.addOperation(ga.TransposedVariable(W2), doGradient=True)
f4 = mainGraph.addOperation(ga.Variable(B2), doGradient=True)

f5 = mainGraph.addOperation(
    ga.MatMatmulOperation(f0, f1),
    doGradient=False,
    finalOperation=False)
f6 = mainGraph.addOperation(
    ga.AddOperation(f5, f2),
    doGradient=False,
    finalOperation=False)

f7 = mainGraph.addOperation(
    ga.MatMatmulOperation(f6, f3),
    doGradient=False,
    finalOperation=False)
f8 = mainGraph.addOperation(
    ga.AddOperation(f7, f4),
    doGradient=False,
    finalOperation=False)

f9 = mainGraph.addOperation(
    ga.SoftmaxOperation(f8, axis=1),
    doGradient=False,
    finalOperation=False)

f10 = mainGraph.addOperation(
    ga.QuadratiCcostOperation(f9, labels),
    doGradient=False,
    finalOperation=True)

print(mainGraph)
print(mainGraph.feedForward())
for op in mainGraph:
    print(op.name, op.shape)

for op in mainGraph:
    print("number:", op.name)
    print(op.getValueExt())

print("\nGradients:")
mainGraph.feedBackward()

for op in mainGraph:
    print("number:", op.name)
    try:
        print(op.getGradientExt(op.inputA))
    except AttributeError:
        pass
    try:
        print(op.getGradientExt(op.inputB))
    except AttributeError:
        pass

gradW1 = f1.getGradientExt().copy()
gradB1 = f2.getGradientExt().copy()
gradW2 = f3.getGradientExt().copy()
gradB2 = f4.getGradientExt().copy()

import scipy.optimize
# params = np.hstack((B1.ravel(), W1.ravel(), B2.ravel(), W2.ravel()))
params = mainGraph.unrollGradientParameters()
print(params)
mainGraph.attachParameters(params)
for op in mainGraph.gradientOps:
    print(op, op.getValueExt())


def f(x):
    mainGraph.attachParameters(x)
    return mainGraph.getValue()


numGrad = scipy.optimize.approx_fprime(params, f, 1e-4)

print("Total Grads")
print((numGrad[0:6].reshape(2, 3) - gradW1))
print((numGrad[6:8] - gradB1))
print((numGrad[8:14].reshape(3, 2) - gradW2))
print((numGrad[14:17] - gradB2))


print("Reduced Grads")
print((numGrad[0:6].reshape(2, 3) - gradW1) / gradW1)
print((numGrad[6:8] - gradB1) / gradB1)
print((numGrad[8:14].reshape(3, 2) - gradW2) / gradW2)
print((numGrad[14:17] - gradB2) / gradB2)


# print(params)
# p = mainGraph.unrollGradientParameters()
# print(p)
# mainGraph.attachParameters(p)
# p = mainGraph.unrollGradientParameters()
# print(p)


# p = X.ravel()


# def f(x):
#     mainGraph = ga.Graph()
#     X = x.reshape((3, 3))

#     f0 = mainGraph.addOperation(ga.Variable(X), doGradient=True)

#     f1 = mainGraph.addOperation(
#         ga.SoftmaxOperation(f0, axis=1),
#         doGradient=False,
#         finalOperation=False)
#     f2 = mainGraph.addOperation(
#         ga.SumSquaredOperation(f1),
#         doGradient=False,
#         finalOperation=True)

#     return mainGraph.getValue()

# print("Second Test")
# numGrad = scipy.optimize.approx_fprime(p, f, 1e-6)
# print(numGrad.reshape(3,3))

# mainGraph = ga.Graph()
# f0 = mainGraph.addOperation(ga.Variable(X), doGradient=True)

# f1 = mainGraph.addOperation(
#     ga.SoftmaxOperation(f0, axis=1),
#     doGradient=False,
#     finalOperation=False)
# f2 = mainGraph.addOperation(
#     ga.SumSquaredOperation(f1),
#     doGradient=False,
#     finalOperation=True)

# print(f1.getGradient(f0))
