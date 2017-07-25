"""Graph definition"""
from .coreDataContainers import Variable
from .coreOperation import CostOperation
from .operations.activationOperations import DropoutOperation
import numpy as np


class Graph(object):

    def __init__(self):
        self.operations = []
        self.gradientOps = []
        self.finalOperation = None
        self.costOperation = None
        self.feederOperation = None
        self.endOperations = []

        self.nOperations = 0

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "Computation Graph:\n"
        for op in self.operations:
            output += op.__repr__() + "\n"
        return output

    def __iter__(self):
        return iter(self.operations)

    def addOperation(self, operation, doGradient=False, finalOperation=False, feederOperation=False):
        """Add an operation ot the graph"""
        self.operations.append(operation)
        operation.assignReferenceNumber(self.nOperations)
        self.nOperations += 1

        self.endOperations.append(operation)
        for op in self.endOperations[:]:
            if operation in op.outputs:
                self.endOperations.remove(op)

        if (doGradient):
            if not (isinstance(operation, Variable)):
                raise ValueError("Graph can only provide gradients with respect to variables!\
                    Call individual ops.getGradient(inputOperation) for individual gradients.")
            self.gradientOps.append(operation)
        if (finalOperation):
            self.finalOperation = operation
            if (isinstance(operation, CostOperation)):
                self.costOperation = operation
        if (feederOperation):
            if (isinstance(operation, Variable)):
                self.feederOperation = operation
            else:
                raise ValueError("Only variables can be feeders")
        return operation

    def unrollGradientParameters(self):
        """For each variable (NOT operation) that needs a gradient calculated
        obtain the inouts and unroll them into a nice vector"""
        params = np.empty(0)
        for op in self.gradientOps:
            if isinstance(op, Variable):
                params = np.hstack((params, np.ravel(op.getValueExt())))
        return params

    def attachParameters(self, params):
        """Given a params vector, attach it as data to all variables,
        NOT operations, that need a gradient evaluation"""
        pointer = 0
        for op in self.gradientOps:
            if isinstance(op, Variable):
                nElems = np.size(op.result)
                shaperino = op.shapeExt
                op.assignData(np.reshape(params[pointer: pointer + nElems], shaperino))
                pointer += nElems

    def feedForward(self):
        """feed forwards through the graph obtaining the value
        of the final operation"""
        return self.finalOperation.getValueExt()

    def getValue(self):
        """Reset the graph and feed forwards through the graph obtaining the value
        of the final operation"""
        self.resetAll()
        return self.feedForward()

    def feedBackward(self):
        """Propagate backwards, gathering all the graients"""
        gradients = []
        for op in self.gradientOps:
            gradients.append((op.referenceNumber, op.name, op.getGradientExt()))
        return gradients

    def getGradients(self):
        """Reset th graph and get gradients of the specified variables"""
        self.resetAll()
        return self.feedBackward()

    def makePredictions(self):
        """Get predictions from a cost operation"""
        if self.costOperation is None:
            raise AttributeError("Must add a cost operation")

        # ------ Set all operations to testing
        for op in self.operations:
            op.testing = True
        self.resetAll()
        pred = self.costOperation.makePredictions()
        # ------ Set all operations to training
        for op in self.operations:
            op.testing = False

        return pred

    def unrollGradients(self):
        """Provide gradiens in the same form the unrolled parameters are provided"""
        grads = np.empty(0)
        for op in self.gradientOps:
            if isinstance(op, Variable):
                grads = np.hstack((grads, np.ravel(op.getGradientExt())))
        return grads

    def resetAll(self):
        """Reset all of the operations"""
        for op in self.operations:
            op.reset()

    def printGraph(self):
        """Print out all of the operations"""
        for op in self.operations:
            print(op)
