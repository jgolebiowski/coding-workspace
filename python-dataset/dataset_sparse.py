import os
from random import shuffle

import numpy as np
import scipy.sparse

from parallel import chunks


class SparseDatasetLoaderBase(object):
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
    partition_loader : function(partition : str, input_path : str) -> (scipy.sparse.csr_matrix, tuple, ndarray)
        Function used to load a given partition, they are kept in dataset_backends.py
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    shuffle_partitions : bool
        If True, shuffle partition order before each pass
    parallel_loader : bool
        Determine whether the loader is a parallel one
    max_threads : int
        Nunmber of threads to use
    """

    def __init__(self, path, partitions_list, batch_size, partition_loader, keep_last_batch, shuffle_partitions,
                 parallel_loader, max_threads):

        self.dataset_path = path
        if partitions_list is None:
            partitions_list = os.listdir(path)

        if parallel_loader:
            partitions_list = list(chunks(partitions_list, max_threads))

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

        data, datashape, labels = self.partition_loader(self.partitions_list[0], self.dataset_path)
        partition_length = len(labels)
        if num_examples == -1:
            num_examples = partition_length

        assert (num_examples <= partition_length), "Cannot specify more examples than fit in a single partition"
        data = densify_data(data[0: num_examples], datashape)

        for i in range(num_iterations):
            for idx in range(0, num_examples, self.batch_size):
                dat = data[idx: idx + self.batch_size]
                lab = labels[idx: idx + self.batch_size]
                if self.keep_last_batch:
                    yield dat, lab
                else:
                    if len(lab) == self.batch_size:
                        yield dat, lab


class SparseDatasetLoaderDisk(SparseDatasetLoaderBase):

    def __iter__(self):
        """
        Load the partitions from disk on the fly and feed the batches
        """
        if self.shuffle_partitions:
            shuffle(self.partitions_list)
        carry_over_data = None
        carry_over_labels = None

        for partition in self.partitions_list:
            data, datashape, labels = self.partition_loader(partition, self.dataset_path)
            # data = densify_data(data, datashape)
            partition_length = len(labels)
            starting_index = 0

            if carry_over_labels is not None:
                required_examples = self.batch_size - len(carry_over_labels)
                dat = scipy.sparse.vstack((carry_over_data, data[0: min(required_examples, partition_length)]))
                lab = np.concatenate((carry_over_labels, labels[0: required_examples]), axis=0)

                if len(lab) < self.batch_size:
                    carry_over_data = dat
                    carry_over_labels = lab
                    continue
                else:
                    starting_index = required_examples
                    carry_over_data = None
                    carry_over_labels = None
                    dat = densify_data(dat, datashape)
                    yield dat, lab

            for idx in range(starting_index, partition_length, self.batch_size):
                dat = data[idx: min(idx + self.batch_size, partition_length)]
                lab = labels[idx: min(idx + self.batch_size, partition_length)]

                if len(lab) < self.batch_size:
                    carry_over_data = dat
                    carry_over_labels = lab
                else:
                    dat = densify_data(dat, datashape)
                    yield dat, lab

        if (carry_over_labels is not None) and (self.keep_last_batch):
            carry_over_data = densify_data(carry_over_data, datashape)
            yield carry_over_data, carry_over_labels


class SparseDatasetLoaderMemory(SparseDatasetLoaderBase):

    def __init__(self, *args):
        super(SparseDatasetLoaderMemory, self).__init__(*args)

        if (len(self.partitions_list) > 0):
            all_data = []
            all_labels = []
            for partition in self.partitions_list:
                local_data, datashape, local_labels = self.partition_loader(partition, self.dataset_path)
                all_data.append(local_data)
                all_labels.append(local_labels)

            data = scipy.sparse.vstack(all_data)
            labels = np.concatenate(all_labels, axis=0)
            self.whole_dataset = (data, datashape, labels)
        else:
            self.whole_dataset = ([], [], [])

    def __iter__(self):
        """
        Iterate over the partition already stored in memory
        """
        data, datashape, labels = self.whole_dataset
        num_examples = len(labels)
        minibatch_index = list(range(0, num_examples, self.batch_size))

        if (not self.keep_last_batch) and ((num_examples - minibatch_index[-1] < self.batch_size)):
            minibatch_index.pop()

        if self.shuffle_partitions:
            shuffle(minibatch_index)

        for idx in minibatch_index:
            dat = data[idx: min(idx + self.batch_size, num_examples)]
            lab = labels[idx: min(idx + self.batch_size, num_examples)]
            dat = densify_data(dat, datashape)
            yield dat, lab


def densify_data(data, datashape):
    """
    Given a partition in a sparse format, convert it to a dense format

    Parameters
    ----------
    data : scipy.sparse.csr_matrix
        Data array of shape (n_examples, n_features)
    datashape : tuple
        Shape of each example, should be consistant with n_features

    Returns
    -------
    ndarray
        Data record
    """
    data = data.toarray()
    data = data.reshape((-1,) + datashape)
    return data
