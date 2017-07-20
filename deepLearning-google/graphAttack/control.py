import graphAttack as ga
import numpy as np


"""Control script"""

mainGraph = ga.Graph()

data1 = np.arange(1000)
data2 = np.arange(1000)

data1b = 2
data2b = 10

feeder1a = ga.Variable(data1)
feeder2a = ga.Variable(data2)
operationA = ga.MultiplyOperation(feeder1a, feeder2a)

feeder1b = ga.Variable(data1b)
feeder2b = ga.Variable(data2b)
operationB = ga.MultiplyOperation(feeder1b, feeder2b)

operation3 = ga.MultiplyOperation(operationA, operationB)
print(operation3.get_value())


def f():
    for i in range(1000):
        operationA.get_value()
        operationA.reset()