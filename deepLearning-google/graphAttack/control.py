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
              [2, 3, 4],
              [5, 6, 7]])
W = np.array([[2, 3, 4],
              [2, 3, 4]])
B = np.array([1, 2])

f0 = mainGraph.addOperation(ga.Variable(X), doGradient=False)
f1 = mainGraph.addOperation(ga.Variable(W.T), doGradient=True)
f2 = mainGraph.addOperation(ga.Variable(B), doGradient=True)

f3 = mainGraph.addOperation(
    ga.MatmulOperation(f0, f1),
    doGradient=False,
    finalOperation=False)
f4 = mainGraph.addOperation(
    ga.AddOperation(f3, f2),
    doGradient=False,
    finalOperation=True)

print(mainGraph)
print(mainGraph.feedForward())
for op in mainGraph:
    print(op.name, op.shape)

print("Gradients:")
mainGraph.getGradients()
print(f1.getGradient())
print(f2.getGradient())
