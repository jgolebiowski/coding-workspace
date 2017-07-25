"""Neural networks utilities"""
import numpy as np
from ..coreDataContainers import Variable, TransposedVariable
from ..operations.activationOperations import *
from ..operations.twoInputOperations import *
from ..operations.singleInputOperations import *
from .misc import generateRandomVariable


def addDenseLayer(mainGraph, nOutputNodes,
                  inputOperation=None,
                  activation=ReLUActivation,
                  dropoutRate=0,
                  w=None,
                  b=None):
    """Append a dense layer to the graph"""
    if (inputOperation is None):
        inputOperation = mainGraph.operations[-1]

    if (w is None):
        w = generateRandomVariable(shape=(nOutputNodes, inputOperation.shape[1]), transpose=True)
    else:
        w = TransposedVariable(w)

    if (b is None):
        b = generateRandomVariable(shape=nOutputNodes, transpose=False)
    else:
        b = Variable(b)

    wo = mainGraph.addOperation(w, doGradient=True)
    bo = mainGraph.addOperation(b, doGradient=True)

    mmo = mainGraph.addOperation(MatMatmulOperation(inputOperation, wo),
                                 doGradient=False,
                                 finalOperation=False)
    addo = mainGraph.addOperation(AddOperation(mmo, bo),
                                  doGradient=False,
                                  finalOperation=False)

    if (dropoutRate > 0):
        dpo = mainGraph.addOperation(DropoutOperation(addo, dropoutRate),
                                     doGradient=False,
                                     finalOperation=False)
    else:
        dpo = addo

    acto = mainGraph.addOperation(activation(dpo),
                                  doGradient=False,
                                  finalOperation=False)
    return acto
