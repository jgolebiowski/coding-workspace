import os
import numpy as np
from random import shuffle

from dataset_backends import libsvm_write_partition_sparse_fromdense as write_partition
from dataset_backends import libsvm_load_partition as load_partition
# from dataset_backends import numpy_write_partition as write_partition
# from dataset_backends import numpy_load_partition as load_partition

def write_partition_multiple(data, labels, partition_size, dataset_path, basefile="partition"):
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
    """
    assert (len(data) == len(labels)), "Data must be of the same length as the labels"
    dataset_path = create_directory(dataset_path)
    size = len(labels)

    for idx in range(0, size, partition_size):
        partition_name = "{}-{}".format(basefile, idx)
        write_partition(data[idx: idx + partition_size],
                        labels[idx: idx + partition_size],
                        partition_name,
                        dataset_path)


class DatasetLoader(object):
    """
    A dataset utility for loading contents of a dataset.

    Parameters
    ----------
    path : str
        Path to the dataset dir
    batch_size : int
        Size of mini-batch.
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    partitions_list list[str]
        List of partition names, if none all partitions in a directory are used
    shuffle_partitions : bool
        If True, shuffle partition order before each pass
    """

    def __init__(self, path, batch_size=1, keep_last_batch=True, partitions_list=None, shuffle_partitions=True):
        self.dataset_path = path
        if partitions_list is None:
            self.partitions_list = os.listdir(path)
        else:
            self.partitions_list = partitions_list

        self.batch_size = batch_size
        self.keep_last_batch = keep_last_batch
        self.shuffle_partitions = shuffle_partitions

    def __iter__(self):
        if self.shuffle_partitions:
            shuffle(self.partitions_list)
        carry_over_data = None
        carry_over_labels = None

        for partition in self.partitions_list:
            data, labels = load_partition(partition, self.dataset_path)
            partition_length = len(labels)
            starting_index = 0

            if carry_over_labels is not None:
                required_examples = self.batch_size - len(carry_over_labels)
                dat = np.concatenate((carry_over_data, data[0: required_examples]), axis=0)
                lab = np.concatenate((carry_over_labels, labels[0: required_examples]), axis=0)

                if len(lab) < self.batch_size:
                    carry_over_data = dat
                    carry_over_labels = lab
                    continue
                else:
                    starting_index = required_examples
                    carry_over_data = None
                    carry_over_labels = None
                    yield dat, lab

            for idx in range(starting_index, partition_length, self.batch_size):
                dat = data[idx: idx + self.batch_size]
                lab = labels[idx: idx + self.batch_size]

                if len(lab) < self.batch_size:
                    carry_over_data = dat
                    carry_over_labels = lab
                else:
                    yield dat, lab

        if (carry_over_labels is not None) and (self.keep_last_batch):
            yield carry_over_data, carry_over_labels

    def iterate_single_partition(self, num_examples=-1, num_iterations=1, partition_name=None):
        """
        Iterate over a small subset of examples from the first partition

        Parameters
        ----------
        num_examples : int
            Number of exampels, if -1 all exmaples in the partition are used.
        num_iterations : int
            Number of times ot iterate over the examples
        partition_name : str
            Partition Name to iterate over, if None, the first one is used

        """
        if self.shuffle_partitions:
            shuffle(self.partitions_list)

        if partition_name is None:
            data, labels = load_partition(self.partitions_list[0], self.dataset_path)
        else:
            data, labels = load_partition(partition_name, self.dataset_path)

        partition_length = len(labels)
        if num_examples == -1:
            num_examples = partition_length

        assert (num_examples <= partition_length), "Cannot specify more examples than fit in a single partition"
        for i in range(num_iterations):
            for idx in range(0, num_examples, self.batch_size):
                dat = data[idx: idx + self.batch_size]
                lab = labels[idx: idx + self.batch_size]
                if self.keep_last_batch:
                    yield dat, lab
                else:
                    if len(lab) == self.batch_size:
                        yield dat, lab


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
