import numpy as np
import random
"""A module with the stocastic gradient descent"""


class adaptiveSGD(object):
    """Class that holds most of the funtionalities of the
    adaptive SGD

    Parameters
    ----------
    trainDataset : np.array
        features for each example in a matrix form
        x.shape = (nExamples, nFeatures)

    trainLabels : np.array
        labels for each example in a matrix form and
        in a one-hot notation
        y.shape = (nExamples, nClasses)

    epochs : int
        number of epochs to run the minimizer

    miniBatchSize : int
        size of the mini batch

    initialLearningRate : float
        learning rate

    eraLearningRateUpdate : float
        Updat the G vector using the exponential running average
        G(t+1) = G(t) * eraLearningRateUpdate + grad * (1 - eraLearningRateUpdate)
        NOTE: Set to None to disable and run classic adaGrad

    momentumTerm : float
        Set the Nesterov momentum parameter, set to 0.0 to disable momentum
        NOTE: Disabling momentum by setting it to 0.0 might be beneficial when using eraLRU or adaGrad


    function : float
        Function to minimize that is of form

    (cost, gradient) = function(params, FeaturesMatrix, LabelsMatrix)
    """

    def __init__(self,
                 trainingData=None,
                 trainingLabels=None,
                 param0=None,
                 epochs=None,
                 miniBatchSize=None,
                 initialLearningRate=None,
                 eraLearningRateUpdate=None,
                 momentumTerm=0.9,
                 testFrequency=None,
                 function=None):

        self.trainingData = trainingData
        self.trainingLabels = trainingLabels
        self.params = param0
        self.momentum = np.zeros(len(param0))
        self.testFrequency = testFrequency
        if (self.testFrequency is None):
            self.testFrequency = int(epochs)

        self.epochs = int(epochs)
        self.miniBatchSize = miniBatchSize
        self.initialLearningRate = initialLearningRate
        self.eraLearningRateUpdate = eraLearningRateUpdate
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

    def minimize(self, monitorTrainigCost=True):
        """find the minimum of the function

        Parameters
        ----------

        x0 : vector of initial weights


        monitorTrainigCost : set whether to print cost data
        """

        iterationBetweenTests = int(self.epochs * self.nMiniBatches / self.testFrequency)
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
                if ((iterNo % iterationBetweenTests == 0) and (self.testFrequency != 0)):
                    iterCost /= iterationBetweenTests
                    self.costLists.append(iterCost)
                    print("Mibatch: %d out of %d from epoch: %d out of %d, iterCost is: %e" %
                          (indexMB, self.nMiniBatches, indexE, self.epochs, iterCost))
                    print("\tMean of the learning rate is %0.7e from (%0.5e, %0.5e)" %
                          (np.mean(self.learningRate), np.min(self.learningRate), np.max(self.learningRate)))
                    # TODO print out cross validation cost every time + use it to implement early stopping
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

        # Calculate the decrease in learning rate according to adaGrad

        # Calculating an outer product to get the diagonal is inefficient it turns out
        # self.gMatrix += np.outer(gradient, gradient)
        # self.learningRate = self.initialLearningRate *\
        #     np.sqrt(np.reciprocal(np.diag(self.gMatrix)))

        if (self.eraLearningRateUpdate is not None):
            self.gVector = self.gVector * self.eraLearningRateUpdate +\
                (1 - self.eraLearningRateUpdate) * np.square(gradient)
            self.learningRate = self.initialLearningRate *\
                np.sqrt(np.reciprocal(self.gVector + 1e-6))
        else:
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
