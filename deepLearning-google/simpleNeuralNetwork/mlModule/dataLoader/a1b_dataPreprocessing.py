from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle


"""We'll convert the entire dataset into a 3D array (image index, x, y)
of floating point values - intensities, normalized to have approximately zero
mean and standard deviation ~0.5 to make training easier down the road."""


def loadClass(folder, minNumberImages, imageSize, pixelDepth):
    """Load the data for a single class"""
    dataFiles = os.listdir(folder)
    dataSet = np.ndarray(shape=(len(dataFiles), imageSize, imageSize),
                         dtype=np.float32)
    print("Reading data from", folder)

    examplesNumber = 0
    for dataPointFileName in dataFiles:
        dataPointFile = os.path.join(folder, dataPointFileName)
        try:
            dataPoint = ndimage.imread(dataPointFile).astype(float)
            if (dataPoint.shape != (imageSize, imageSize)):
                raise Exception("Unexpected image shape %s" % str(dataPoint.shape))
            dataSet[examplesNumber, :, :] = dataPoint
            examplesNumber += 1
        except IOError as e:
            print('Could not read:', dataPointFile, ':', e, '- it\'s ok, skipping.')

    dataSet = dataSet[0:examplesNumber, :, :]
    if (examplesNumber < minNumberImages):
        raise Exception("Many fewer examples: %d < %d" % (examplesNumber, minNumberImages))

    print('Full dataset tensor:', dataSet.shape)

    # mean = np.mean(dataSet, axis=0)
    # sigma = np.std(dataSet, axis=0)

    mean = np.ones(dataSet[0].shape) * pixelDepth / 2
    sigma = np.ones(dataSet[0].shape) * pixelDepth
    dataSet -= mean
    dataSet /= sigma[None, :, :]

    meanAll = np.mean(dataSet)
    sigmaAll = np.std(dataSet)
    print('Mean:', meanAll)
    print('Standard deviation:', sigmaAll)
    return dataSet, mean, sigma


def loadAndPickleDataSet(dataSetDirectory, minExamplesPerClass, imageSize, pixelDepth, force=False):
    """Load a whole dataset and picle it"""
    dataSetFolders = [dataSetDirectory + "/" +
                      item for item in os.listdir(dataSetDirectory) if ".pkl" not in item]
    dataSetClasses = []
    for folder in dataSetFolders:
        classFileName = folder + ".pkl"
        dataSetClasses.append(classFileName)
        if ((os.path.exists(classFileName)) and (not force)):
            print('%s already present - Skipping pickling.' % classFileName)
        else:
            print('Pickling %s.' % classFileName)
            # dataSet, mean, sigma = loadClass(folder, minExamplesPerClass)
            dataSet = loadClass(folder, minExamplesPerClass, imageSize, pixelDepth)

            with open(classFileName, "wb") as fp:
                pickle.dump(dataSet, fp, pickle.HIGHEST_PROTOCOL)

    return dataSetClasses


if __name__ == "__main__":
    imageSize = 28
    pixelDepth = 255.0

    clasNamesTest = loadAndPickleDataSet("dataSet/notMNIST_large", 45000, imageSize, pixelDepth, force=True)
    clasNamesTrain = loadAndPickleDataSet("dataSet/notMNIST_small", 1700, imageSize, pixelDepth, force=True)

    # Test data
    doTest = False
    index = 1
    if (doTest):
        with open(clasNames[index], "rb") as fp:
            testData = pickle.load(fp)
        plt.imshow(testData[0][0])
        plt.show()
