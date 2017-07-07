"""Assignement 1a - getting the data"""
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

url = 'https://commondatastorage.googleapis.com/books1000/'
prefix = "dataSet"


def downloadDataToFile(fileName, expectedBytes, force=False):
    """Download a file and check if it has the right number of bytes"""
    destination = os.path.join(prefix, fileName)
    if ((force) or (not os.path.exists(destination))):
        print("Attempting to download", fileName)
        fileName, temp = urlretrieve(url + fileName, destination, reporthook=None)
        print("Download complete!")

    fileInfo = os.stat(destination)
    if (fileInfo.st_size == expectedBytes):
        print("Found and verified", destination)
    else:
        raise Exception("Failed to verify " + destination + " :(")
    return destination


train_filename = downloadDataToFile('notMNIST_large.tar.gz', 247336696)
test_filename = downloadDataToFile('notMNIST_small.tar.gz', 8458043)
