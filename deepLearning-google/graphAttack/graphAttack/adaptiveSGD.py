import numpy as np
import random
"""A module with the stocastic gradient descent"""


class adaptiveSGD(object):
    """Class that holds most of the funtionalities of the
    adaptive SGD

    Parameters
    ----------
    trainDataset : features for each example in a matrix form
        x.shape = (nExamples, nFeatures)

    trainLabels : labels for each example in a matrix form and
        in a one-hot notation
        y.shape = (nExamples, nClasses)

    epochs : number of epochs to run the minimizer

    miniBatchSize : size of the mini batch

    learningRate : learning rate

    function : Function to minimize that is of form

    (cost, gradient) = function(params, FeaturesMatrix, LabelsMatrix)
    """

    def __init__(self,
                 trainingData=None,
                 trainingLabels=None,
                 param0=None,
                 epochs=None,
                 miniBatchSize=None,
                 initialLearningRate=None,
                 momentumTerm=0.9,
                 function=None):

        self.trainingData = trainingData
        self.trainingLabels = trainingLabels
        self.params = param0
        self.momentum = np.zeros(len(param0))

        self.epochs = int(epochs)
        self.miniBatchSize = miniBatchSize
        self.initialLearningRate = initialLearningRate
        self.learningRate = np.ones(len(param0)) * initialLearningRate
        self.momentumTerm = momentumTerm
        self.gVector = np.ones(len(param0)) * 1e-8

        self.nMiniBatches = int(len(trainingData) / miniBatchSize)
        self.miniBatchIndexList = list(range(0, len(trainingData), self.miniBatchSize))

        self.trainingDataBatchesIndex = [(index, index + self.miniBatchSize)
                                         for index in self.miniBatchIndexList]
        self.trainingLabelsBatchesIndex = [(index, index + self.miniBatchSize)
                                           for index in self.miniBatchIndexList]

        self.func = function

    def minimize(self, monitorTrainigCost=0):
        """find the minimum of the function

        Parameters
        ----------

        x0 : vector of initial weights


        monitorTrainigCost : set how often to print cost data,
            0 for no printout
            1 for 1 printout per training
            10 for 10 printouts per training
        """

        iterationsToPrint = int(self.epochs * self.nMiniBatches / monitorTrainigCost)
        self.costLists = []
        iterCost = 0
        randomMiniBatchIndexList = list(range(self.nMiniBatches))

        for indexE in range(self.epochs):
            random.shuffle(randomMiniBatchIndexList)

            for indexMB in range(self.nMiniBatches):
                iterNo = indexE * self.nMiniBatches + indexMB
                randBatchIndex = randomMiniBatchIndexList[indexMB]
                mBatchBeggining = self.trainingDataBatchesIndex[randBatchIndex][0]
                mBatchEnd = self.trainingDataBatchesIndex[randBatchIndex][1]

                cost = self.updateMiniBatch(self.params,
                                            self.trainingData[mBatchBeggining: mBatchEnd],
                                            self.trainingLabels[mBatchBeggining: mBatchEnd])

                iterCost += cost
                if ((iterNo % iterationsToPrint == 0) and (monitorTrainigCost != 0)):
                    iterCost /= iterationsToPrint
                    self.costLists.append(iterCost)
                    print("Mibatch: %d out of %d from epoch: %d out of %d, iterCost is: %e" %
                          (indexMB, self.nMiniBatches, indexE, self.epochs, iterCost))
                    # print "Median of the learning rate is", np.median(self.learningRate)
                    iterCost = 0

        return self.params

    def updateMiniBatch(self, params, X, Y):
        """ Make an update with a small batch

        Parameters
        ----------

        params : vector of parameters for the function

        X : features for each example in a matrix form
           x.shape = (nExamples, nFeatures)

        Y : labels for each example in a matrix form and
           in a one-hot notation
           y.shape = (nExamples, nClasses)

        """

        # Update the parameters according to Nesterov accelerated gradient
        paramsNAG = params - self.momentum * self.learningRate
        cost, gradient = self.func(paramsNAG, X, Y)
        print(cost)
        print(gradient)

        # Calculate the decrease in learning rate according to adaGrad

        # Calculating an outer product to get the diagonal is inefficient it turns out
        # self.gMatrix += np.outer(gradient, gradient)
        # self.learningRate = self.initialLearningRate *\
        #     np.sqrt(np.reciprocal(np.diag(self.gMatrix)))

        self.gVector += np.square(gradient)
        self.learningRate = self.initialLearningRate *\
            np.sqrt(np.reciprocal(self.gVector))

        # Calculate momentum to evaluate the change in parameters
        changeInMomentum = np.multiply(self.learningRate, gradient)
        self.momentum = self.momentum * self.momentumTerm + changeInMomentum
        updateValue = self.momentum

        # Use the update value to updae the parameters
        params = params - updateValue
        self.params = params
        return cost
