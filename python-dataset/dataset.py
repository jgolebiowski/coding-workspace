import multiprocessing
import os
from random import shuffle

import numpy as np

from dataset_backends import libsvm_load_partition, \
    libsvm_load_partition_sparse, libsvm_load_partition_sparse_parallel
from dataset_backends import numpy_load_partition
from dataset_sparse import SparseDatasetLoaderDisk, SparseDatasetLoaderMemory


def DatasetLoaderFactory(path,
                         partitions_list=None,
                         partition_loader=None,
                         batch_size=1,
                         keep_last_batch=True,
                         shuffle_partitions=True,
                         save_in_memory=False,
                         max_threads=None):
    """
    Create a dataset utility for loading contents of a dataset.

    Parameters
    ----------
    path : str
        Path to the dataset dir
    partitions_list : list[str]
        List of partition names, if none all partitions in a directory are used
    partition_loader : str
        Specify the partition loder using a string, current options are:
        "numpy"
        "libsvm-dense"
        "libsvm-sparse"
        "libsvm-sparse-parallel"
    batch_size : int
        Size of mini-batch.
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    shuffle_partitions : bool
        If True, shuffle partition order before each pass
    save_in_memory : bool
        If true, save the loaded dataset so that it wont have to be re-read every epoch
    max_threads : int
        Maximum number of threads ot use is a parallel loader is specified

    Returns
    -------
    DatasetLoader
        DatasetLoader ready to use.
    """
    if partition_loader == "numpy":
        loader = numpy_load_partition
        if save_in_memory:
            return DenseDatasetLoaderMemory(path, partitions_list, batch_size, loader, keep_last_batch,
                                            shuffle_partitions)
        else:
            return DenseDatasetLoaderDisk(path, partitions_list, batch_size, loader, keep_last_batch,
                                          shuffle_partitions)

    elif partition_loader == "libsvm-dense":
        loader = libsvm_load_partition
        if save_in_memory:
            return DenseDatasetLoaderMemory(path, partitions_list, batch_size, loader, keep_last_batch,
                                            shuffle_partitions)
        else:
            return DenseDatasetLoaderDisk(path, partitions_list, batch_size, loader, keep_last_batch,
                                          shuffle_partitions)

    elif partition_loader == "libsvm-sparse":
        loader = libsvm_load_partition_sparse
        parallel_loader = False
        if save_in_memory:
            return SparseDatasetLoaderMemory(path, partitions_list, batch_size, loader, keep_last_batch,
                                             shuffle_partitions, parallel_loader, max_threads)
        else:
            return SparseDatasetLoaderDisk(path, partitions_list, batch_size, loader, keep_last_batch,
                                           shuffle_partitions, parallel_loader, max_threads)

    elif partition_loader == "libsvm-sparse-parallel":
        loader = libsvm_load_partition_sparse_parallel
        parallel_loader = True
        if max_threads is None:
            max_threads = int(multiprocessing.cpu_count() / 2)

        if save_in_memory:
            return SparseDatasetLoaderMemory(path, partitions_list, batch_size, loader, keep_last_batch,
                                             shuffle_partitions, parallel_loader, max_threads)
        else:
            return SparseDatasetLoaderDisk(path, partitions_list, batch_size, loader, keep_last_batch,
                                           shuffle_partitions, parallel_loader, max_threads)

    else:
        raise ValueError("Wrong partition loader specified")


class DenseDatasetLoaderBase(object):
    """
    A dataset utility for loading contents of a dataset.

    Parameters
    ----------
    path : str
        Path to the dataset dir
    partitions_list list[str]
        List of partition names, if none all partitions in a directory are used
    batch_size : int
        Size of mini-batch.
    partition_loader : function(partition : str, input_path : str) -> (ndarray, ndarray)
        Function used to load a given partition, they are kept in dataset_backends.py
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    shuffle_partitions : bool
        If True, shuffle partition order before each pass
    """

    def __init__(self, path, partitions_list, batch_size, partition_loader, keep_last_batch, shuffle_partitions):

        self.dataset_path = path
        if partitions_list is None:
            partitions_list = os.listdir(path)

        self.partitions_list = partitions_list
        self.batch_size = batch_size
        self.keep_last_batch = keep_last_batch
        self.shuffle_partitions = shuffle_partitions
        self.partition_loader = partition_loader

    def iterate_single_partition(self, num_examples=-1, num_iterations=1):
        """
        Iterate over a small subset of examples from the first partition

        Parameters
        ----------
        num_examples : int
            Number of exampels, if -1 all exmaples in the partition are used.
        num_iterations : int
            Number of times ot iterate over the examples

        """
        if self.shuffle_partitions:
            shuffle(self.partitions_list)

        data, labels = self.partition_loader(self.partitions_list[0], self.dataset_path)
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


class DenseDatasetLoaderDisk(DenseDatasetLoaderBase):

    def __iter__(self):
        """
        Load the partitions from disk on the fly and feed the batches
        """
        if self.shuffle_partitions:
            shuffle(self.partitions_list)
        carry_over_data = None
        carry_over_labels = None

        for partition in self.partitions_list:
            data, labels = self.partition_loader(partition, self.dataset_path)
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


class DenseDatasetLoaderMemory(DenseDatasetLoaderBase):

    def __init__(self, *args):
        super(DenseDatasetLoaderMemory, self).__init__(*args)

        if (len(self.partitions_list) > 0):
            all_data = []
            all_labels = []
            for partition in self.partitions_list:
                local_data, local_labels = self.partition_loader(partition, self.dataset_path)
                all_data.append(local_data)
                all_labels.append(local_labels)

            data = np.concatenate(all_data, axis=0)
            labels = np.concatenate(all_labels, axis=0)
            self.whole_dataset = (data, labels)
        else:
            self.whole_dataset = ([], [])

    def __iter__(self):
        """
        Iterate over the partition already stored in memory
        """
        data, labels = self.whole_dataset
        num_examples = len(labels)
        minibatch_index = list(range(0, num_examples, self.batch_size))

        if (not self.keep_last_batch) and ((num_examples - minibatch_index[-1] < self.batch_size)):
            minibatch_index.pop()

        if self.shuffle_partitions:
            shuffle(minibatch_index)

        for idx in minibatch_index:
            dat = data[idx: idx + self.batch_size]
            lab = labels[idx: idx + self.batch_size]
            yield dat, lab
