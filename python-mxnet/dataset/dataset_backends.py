import os

import numpy as np
import scipy.sparse
import sklearn.datasets


def libsvm_write_partition_sparse_fromdense(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset, wrapper around libsvm_write_partition_sparse to be compatible with tests

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"
    datashape = data[0].shape
    dat = [scipy.sparse.csr_matrix(item.reshape((1, -1))) for item in data]
    lab = np.array(labels)
    libsvm_write_partition_sparse(dat, datashape, lab, partition_name, dataset_path)


def libsvm_write_partition_sparse(data, datashape, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : list[scipy.sparse.csr_matrix]
        List of sparse representations of the array as a (1, example_size) matrix
    datashape : tuple
        Shape of each example
    labels : ndarray or list
        The labels for this data. Shape: (n_examples, )
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    data = scipy.sparse.vstack(data)
    partition = os.path.join(dataset_path, partition_name) + ".libsvm"
    comment = "${}$".format(datashape)
    sklearn.datasets.dump_svmlight_file(data, labels, partition, zero_based=True, comment=comment)


def libsvm_write_partition_dense(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"

    if type(data) == list:
        data = np.array(data)
    if type(labels) == list:
        labels = np.array(labels)

    partition = os.path.join(dataset_path, partition_name) + ".libsvm"
    datashape = data.shape
    comment = "${}$".format(datashape[1:])
    sklearn.datasets.dump_svmlight_file(data.reshape((datashape[0], -1)), labels, partition, zero_based=True,
                                        comment=comment)


def libsvm_load_partition(partition, input_path):
    """
    Load a partition and return the data and labels

    Parameters
    ----------
    partition : str
        Name of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    ndarray
        Data record
    ndarray
        Labels
    """
    assert partition.endswith(".libsvm"), "File must be a .libsvm one"
    partition = os.path.join(input_path, partition)

    with open(partition, "r") as file:
        for i in range(4):
            comment = file.readline()
    datashape = eval(comment.split("$")[1])
    datasize = 1
    for elm in datashape:
        datasize *= elm

    data, labels = sklearn.datasets.load_svmlight_file(partition, n_features=datasize, dtype=np.float32,
                                                       zero_based=True)
    data = data.toarray()
    data = data.reshape((-1,) + datashape)
    return data, labels


def numpy_write_partition(data, labels, partition_name, dataset_path):
    """
    Write a new record to the dataset

    Parameters
    ----------
    data : ndarray or list[ndarray]
        Data to be stored. Shape: (nexamples, ...)
        Alternatively: list[ndarray] with one array for each example
    labels : ndarray or list
        The labels for this data. Shape: (nexamples, )
        Alternatively: list with one input for each example
    partition_name : str
        Id of the partition, should be uniqie or it will be overwritten
    dataset_path : str
        Path to the dataset directory
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"

    if type(data) == list:
        data = np.array(data)
    if type(labels) == list:
        labels = np.array(labels)

    partition = os.path.join(dataset_path, partition_name)
    np.savez(partition, data=data, labels=labels)


def numpy_load_partition(partition, input_path):
    """
    Load a partition and return the data and labels

    Parameters
    ----------
    partition : str
        Name of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    ndarray
        Data record
    ndarray
        Labels
    """
    assert partition.endswith(".npz"), "File must be a .npz one"
    partition = os.path.join(input_path, partition)
    with np.load(partition) as part:
        data = part["data"]
        labels = part["labels"]
    return data, labels
