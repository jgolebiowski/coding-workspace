"""Assignement 1a - getting the data"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from scipy import ndimage
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

np.random.seed(133)


def downloadDataToFile(fileName, expectedBytes, prefix, url, force=False):
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


def maybe_extract(filename, prefix, num_classes, force=False):
    root = os.path.splitext(os.path.splitext(filename)[0])[0]  # remove .tar.gz
    if os.path.isdir(root) and not force:
        # You may override by setting force=True.
        print('%s already present - Skipping extraction of %s.' % (root, filename))
    else:
        print('Extracting data for %s. This may take a while. Please wait.' % root)
        tar = tarfile.open(filename)
        sys.stdout.flush()
        tar.extractall(prefix)
        tar.close()
    data_folders = [
        os.path.join(root, d) for d in sorted(os.listdir(root))
        if os.path.isdir(os.path.join(root, d))]
    if len(data_folders) != num_classes:
        raise Exception(
            'Expected %d folders, one per class. Found %d instead.' % (
                num_classes, len(data_folders)))
    print(data_folders)
    return data_folders


if __name__ == "__main__":
    url = 'https://commondatastorage.googleapis.com/books1000/'
    prefix = "dataSet"

    train_filename = downloadDataToFile('notMNIST_large.tar.gz', 247336696, prefix, url)
    test_filename = downloadDataToFile('notMNIST_small.tar.gz', 8458043, prefix, url)

    num_classes = 10

    train_folders = maybe_extract(train_filename, prefix, num_classes)
    test_folders = maybe_extract(test_filename, prefix, num_classes)
