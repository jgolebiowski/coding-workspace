import os
import numpy as np
from random import shuffle
from dataset_backends import numpy_load_partition




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
    partition_loder : function(partition : str, input_path : str) -> ndarray, ndarray
        Function used to load a given partition, they are kept in dataset_backends.py
    """

    def __init__(self, path, batch_size=1, keep_last_batch=True, partitions_list=None, shuffle_partitions=True, partition_loder=None):
        if partition_loder is None:
            partition_loder = numpy_load_partition
        self.partition_loader = partition_loder

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

        # TODO Maybe add a functonality to load the next partition in the background while current one is being loaded
        # if first_iteration:
        #     data, labels = self.partition_loader()
        #     start_loading_next_partition()
        #     first_iteration = False
        # else:
        #     data, labels = get_partition_from_loader()
        #     start_loading_next_partition()


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
            data, labels = self.partition_loader(self.partitions_list[0], self.dataset_path)
        else:
            data, labels = self.partition_loader(partition_name, self.dataset_path)

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

