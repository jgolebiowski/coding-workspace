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


X = np.array([[1, 2, 3],
              [2, 10, 4],
              [5, 6, 7]])
W1 = np.array([[2, 3, 4],
               [2, 10, 4]])
B1 = np.array([1, 2])

W2 = np.array([[1, 3],
               [2, 3],
               [10, 20]])
B2 = np.array([1, 2, 3])

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
    ga.SumSquaredOperation(f8),
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


import scipy.optimize
params = np.hstack((B1.ravel(), W1.ravel(), B2.ravel(), W2.ravel()))
print(params)


def f(x):
    mainGraph = ga.Graph()
    X = np.array([[1, 2, 3],
                  [2, 10, 4],
                  [5, 6, 7]])

    W1 = x[2:8].reshape(2, 3)
    B1 = x[0:2]

    W2 = x[11:17].reshape(3, 2)
    B2 = x[8:11]

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
        ga.SumSquaredOperation(f8),
        doGradient=False,
        finalOperation=True)

    return mainGraph.getValue()


numGrad = scipy.optimize.approx_fprime(params, f, 1e-6)
print(numGrad[2:8].reshape(2, 3))
print(numGrad[0:2])
print(numGrad[11:17].reshape(3, 2))
print(numGrad[8:11])
