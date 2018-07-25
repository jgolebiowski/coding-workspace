import os

import numpy as np
import scipy.sparse
import sklearn.datasets

from parallel import parallel_control


def write_partition_multiple(data, labels, partition_size, dataset_path, basefile="partition", writer=None):
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
    partition_size : int
        Number of examples in a partition
    dataset_path : str
        Path to the dataset directory
    basefile : int
        Base of the partition names, should be uniqie or it will be overwritten
    partition_loder : function(data : ndarray, labels : ndarray, partition_name : str, dataset_path : str)
        Function used to write a partition
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"
    if writer is None:
        writer = libsvm_write_partition

    dataset_path = create_directory(dataset_path)
    size = len(labels)

    partition_index = 0
    for idx in range(0, size, partition_size):
        partition_name = "{}-{}".format(basefile, partition_index)
        partition_index += 1
        writer(data[idx: idx + partition_size],
               labels[idx: idx + partition_size],
               partition_name,
               dataset_path)


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


def libsvm_write_partition(data, labels, partition_name, dataset_path):
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

    partition_dir = create_directory(os.path.join(dataset_path, partition_name))
    data_file = os.path.join(partition_dir, "data.libsvm")

    datashape = data.shape[1:]
    n_examples = data.shape[0]

    with open(data_file, "wb") as dfile:
        sklearn.datasets.dump_svmlight_file(data.reshape((n_examples, -1)), labels, dfile, zero_based=True)

    header = "datashape${}\n".format(datashape)
    header_file = os.path.join(partition_dir, "header.libsvm")
    with open(header_file, "wb") as hfile:
        hfile.write(header.encode())


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
    data, datashape, labels = libsvm_load_partition_sparse(partition, input_path)
    data = data.toarray()
    data = data.reshape((-1,) + datashape)
    return data, labels


def libsvm_load_partition_sparse_parallel(partition_list, input_path):
    """
    Load multiple partitions and return the data and labels

    Parameters
    ----------
    partition_list : list[str]
        List of names of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    scipy.sparse.csr_matrix
        Data array of shape (n_examples, n_features)
    tuple
        Shape of each example, should be consistant with n_features
    ndarray
        Labels
    """
    assert type(partition_list) == list, "Must set the parallel_load flag to True to use parallel loaders"
    results = parallel_control(libsvm_load_partition_sparse,
                               [(item,) for item in partition_list],
                               fixed_args=(input_path,),
                               start_method="fork")

    labels = [item[1][2] for item in results]
    labels = np.concatenate(labels, axis=0)

    datashape = results[0][1][1]
    data = [item[1][0] for item in results]
    data = scipy.sparse.vstack(data)
    return data, datashape, labels


def libsvm_load_partition_sparse(partition, input_path):
    """
    Load a partition and return the data in sparse format and labels

    Parameters
    ----------
    partition : str
        Name of the dataset chunks
    input_path : str
        path to the dataset directory

    Returns
    -------
    scipy.sparse.csr_matrix
        Data array of shape (n_examples, n_features)
    tuple
        Shape of each example, should be consistant with n_features
    ndarray
        Labels
    """
    partition = os.path.join(input_path, partition)
    data_file = os.path.join(partition, "data.libsvm")
    header_file = os.path.join(partition, "header.libsvm")

    assert os.path.isfile(data_file), "Partition must contain data.libsvm"
    assert os.path.isfile(header_file), "Partition must contain header.libsvm"

    with open(header_file, "rb") as hfile:
        header_str = hfile.readlines()

    header = {}
    for elm in header_str:
        single = elm.decode().split("$")
        header[single[0]] = eval(single[1])

    datasize = 1
    for elm in header["datashape"]:
        datasize *= elm

    with open(data_file, "rb") as dfile:
        data, labels = sklearn.datasets.load_svmlight_file(dfile, n_features=datasize, dtype=np.float32,
                                                           zero_based=True)
    return data, header["datashape"], labels


def create_directory(name):
    """
    Create a directory

    Parameters
    ----------
    name : str
        Directory name

    Returns
    -------
    str
        Path to the newly created direcotry
    """
    try:
        os.mkdir(name)
    except OSError:
        pass
    return name
