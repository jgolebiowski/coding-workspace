"""Node definition"""
import numpy as np


class Node(object):
    """Node - a basic building block of the graph"""
    shape = None
    name = "Node"
    referenceNumber = None

    def __init__(self):
        self.outputs = []
        self.result = None
        self.endNode = True

    def __repr__(self):
        """Represent as a string - usefull for printing"""
        output = "<%s>" % self.name
        return output

    def prependName(self, string):
        """Prepend name with a string"""
        self.name = str(string) + self.name

    def assignReferenceNumber(self, number):
        """Assign a record number"""
        self.referenceNumber = number
        self.prependName("op" + str(number) + "-")

    def setShape(self):
        """Set the shape of the output of this node"""
        raise NotImplementedError("This is an abstract class, this routine should be implemented in children")

    def addOutput(self, output):
        """Attach the node that is the output of this Node"""
        self.outputs.append(output)
        self.endNode = False

    def reset(self):
        """Reset the values and gradients held by this operation"""
        raise NotImplemented("This is an abstract class")

    def getValue(self):
        """Return a vaue of this operation"""
        if (self.result is None):
            raise NotImplemented("The result is not set at initialization, maybe use an operation")
        return self.result


def broadcast_shape(shp1, shp2):
    """Broadcast the shape of those arrays"""
    try:
        return np.broadcast(np.empty(shp1), np.empty(shp2)).shape
    except ValueError:
        raise ValueError("Arrays cannot be broadcasted - %s and %s " % (str(shp1), str(shp2)))


def reduce_shape(inputArr, targetArr):
    """Reduce the dimensions by summing over necesary axis"""
    if (inputArr.shape == targetArr.shape):
        return inputArr

    try:
        if (inputArr.shape[1] == targetArr.shape[0]):
            return np.sum(inputArr, axis=0)
    except (IndexError):
        pass
    except (TypeError):
        pass

    try:
        if (inputArr.shape[0] == targetArr.shape[1]):
            return np.sum(inputArr, axis=1)
    except (IndexError):
        pass
    except (TypeError):
        pass

    raise ValueError("The two arrays cannot be reduced properly")
