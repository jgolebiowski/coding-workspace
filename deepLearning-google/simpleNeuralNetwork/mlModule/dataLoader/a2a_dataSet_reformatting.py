
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
from . import a1b_dataPreprocessing as a1b

"""Generate training, cross-validation and test sets"""
# imageSize = 28
# pixelDepth = 255.0
# prefix = "dataSet"


def reformatDataSet(dataset, labels):
    """Given a dataset in a format
    (x, y)
    where :
    x - features
    y - labels

    with each example:
    x - np.array as a matrix
    y - int baing a label

    returns
    (x, y)
    where:
    x - large matrix of all examples and
    x.shape = (nExamples, nFeatures)

    y - one-hot labelled data for each exampe
    y.shape = (nExamples, nClasses)
    entry with an index corresponding to the label is 1, rest are 0"""

    # Create new arrays
    nExamples = len(labels)
    nFeatures = len(dataset[0].ravel())
    nClasses = np.max(labels) + 1

    newDataset = np.empty((nExamples, nFeatures), dtype=dataset.dtype)
    newLabels = np.zeros((nExamples, nClasses), dtype=int)
    for i in range(nExamples):
        newDataset[i, :] = dataset[i].ravel()
        newLabels[i, labels[i]] = 1

    return newDataset, newLabels


if __name__ == "__main__":
    pickleFilename = "dataSet/notMNIST.pickle"
    with open(pickleFilename, "rb") as fp:
        allDatasets = pickle.load(fp)

    testDataset = allDatasets["test_dataset"]
    testLabels = allDatasets["test_labels"]
    reformTestDataset, reformTestLabels = reformatDataSet(testDataset, testLabels)

    validDataset = allDatasets["valid_dataset"]
    validLabels = allDatasets["valid_labels"]
    reformvalidDataset, reformvalidLabels = reformatDataSet(validDataset, validLabels)

    trainDataset = allDatasets["train_dataset"]
    trainLabels = allDatasets["train_labels"]
    reformtrainDataset, reformtrainLabels = reformatDataSet(trainDataset, trainLabels)

    pickleFilenameReformed = "dataSet/notMNISTreformatted.pkl"
    try:
        f = open(pickleFilenameReformed, 'wb')
        save = {
            'trainDataset': reformtrainDataset,
            'trainLabels': reformtrainLabels,
            'validDataset': reformvalidDataset,
            'validLabels': reformvalidLabels,
            'testDataset': reformTestDataset,
            'testLabels': reformTestLabels,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickleFilenameReformed, ':', e)
        raise
