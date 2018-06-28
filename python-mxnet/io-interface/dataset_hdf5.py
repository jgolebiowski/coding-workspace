import h5py
import numpy as np
import mxnet as mx


class HDF5Generator(object):
    """
    Generate a HDF5 Dataset form a given data

    Parameters
    ----------
    filepath : str
        Path to the dataset file

    """

    def __init__(self, filepath):
        if filepath.endswith(".hdf5"):
            self.hdf5 = h5py.File(filepath, "w")
        else:
            self.hdf5 = h5py.File(filepath + ".hdf5", "w")

        self.id = 0

    def __del__(self):
        self.hdf5.close()

    def initialize_from_data(self, data, labels):
        """
        Initialize the dataset from data.
        WARNING!
        initialize_empty() -> write_single() is faster for lists
        initialize_from_data() is faster for numpy arrays

        Parameters
        ----------
        data : ndarray or list[ndarray]
            Data to be stored. Shape: (nexamples, ...)
            Alternatively: list[ndarray] with one array for each example
        labels : ndarray or list
            The labels for this data. Shape: (nexamples, )
            Alternatively: list with one input for each example

        """
        if len(data) != len(labels):
            raise ValueError("Lengths of data and labels must be equal")

        if type(data) == list:
            data = np.array(data)
        if type(labels) == list:
            labels = np.array(labels)

        self.hdf5.create_dataset("data", data=data)
        self.hdf5.create_dataset("labels", data=labels)

    def initalize_empty(self, length, element_shape, dtype):
        """
        Initialize an empty dataset

        Parameters
        ----------
        length : int
            Number of examples
        element_shape : tuple[int]
            Shape of each example data
        dtype : np.dtype
            Datatype for the dataset
        """
        shape = (length, ) + element_shape
        self.data = self.hdf5.create_dataset("data", shape=shape, dtype=dtype)
        self.labels = self.hdf5.create_dataset("labels", shape=(length, ), dtype=dtype)
        self.current_pos = 0
        self.dtype = dtype

    def write_single(self, data, label):
        """
        Write a new record to the dataset

        Parameters
        ----------
        data : ndarray
            Data to be stored, should be in "C" order (Row Major) and in the
            dtype specified in self.dtype
        label : int
            The label for this data
        """
        self.data[self.current_pos, :] = data.astype(self.dtype)
        self.labels[self.current_pos] = label
        self.current_pos += 1


class HDF5Loader(object):
    """
    A dataset utility for loading contents of a HDF5 file written by HDF5Generator.

    Parameters
    ----------
    filepath : str
        Path to the dataset record file
    batch_size : int
        Size of mini-batch.
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    """

    def __init__(self, filepath, batch_size=1, keep_last_batch=True):
        if filepath.endswith(".hdf5"):
            self.hdf5 = h5py.File(filepath, "r")
        else:
            self.hdf5 = h5py.File(filepath + ".hdf5", "r")

        self.batch_size = batch_size
        self.keep_last_batch = keep_last_batch
        self.current_position = 0
        self.dataset_length = len(self.hdf5["data"])

        self.data = self.hdf5["data"]
        self.labels = self.hdf5["labels"]

    def __del__(self):
        self.hdf5.close()

    def __iter__(self):
        self.current_position = 0
        return self

    def __next__(self):
        if self.current_position >= self.dataset_length:
            raise StopIteration

        # data = self.hdf5["data"][self.current_position: self.current_position + self.batch_size]
        # labels = self.hdf5["labels"][self.current_position: self.current_position + self.batch_size]

        data = self.data[self.current_position: self.current_position + self.batch_size]
        labels = self.labels[self.current_position: self.current_position + self.batch_size]

        if not self.keep_last_batch:
            if len(data) < self.batch_size:
                raise StopIteration

        self.current_position += self.batch_size
        return mx.nd.array(data), mx.nd.array(labels)
