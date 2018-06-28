import os
import numpy as np
import mxnet as mx


class CSVGenerator(object):
    """
    Initialize an empty CSV dataset

    Parameters
    ----------
    path : str
        Path to the dataset dir
    data_element_shape : tuple[int]
        Shape of each example data
    dtype : str
        Datatype for the dataset given in string format i.e. "float32"
    precision : int
        Floating point precision.
    """

    def __init__(self, path, data_element_shape, dtype, precision=5):
        dataset = create_directory(path)
        self.data = open(os.path.join(dataset, "data.csv"), "w")
        self.labels = open(os.path.join(dataset, "labels.csv"), "w")

        with open(os.path.join(dataset, "manifest.txt"), "w") as manifest:
            properties = dict(data_element_shape=data_element_shape,
                              dtype=dtype)
            manifest.write(str(properties))

        self.precision=precision

    def __del__(self):
        self.data.close()
        self.labels.close()

    def finalise(self):
        """
        Finalise writing
        """
        self.__del__()

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
        datasize = data.size
        self.data.write(np.array2string(data.ravel(),
                                        separator=";",
                                        max_line_width=np.inf,
                                        threshold=np.inf,
                                        precision=self.precision,
                                        suppress_small=True,
                                        )[1:-1] + os.linesep)
        self.labels.write(str(label) + os.linesep)


class CSVLoader(object):
    """
    A dataset utility for loading contents of a CSV file written by CSVGenerator.

    Parameters
    ----------
    path : str
        Path to the dataset dir
    batch_size : int
        Size of mini-batch.
    keep_last_batch : bool
        If True, keep last batch even if it will be smaller than batch_size,
        If False, discard it
    """

    def __init__(self, path, batch_size=1, keep_last_batch=True):
        self.data = open(os.path.join(path, "data.csv"), "r")
        self.labels = open(os.path.join(path, "labels.csv"), "r")

        self.batch_size = batch_size
        self.keep_last_batch =  keep_last_batch

        with open(os.path.join(path, "manifest.txt"), "r") as manifest:
            self.properties = eval(manifest.readline())

    def __del__(self):
        self.data.close()
        self.labels.close()

    def __iter__(self):
        return self

    def __next__(self):
        data = []
        labels = []
        for idx in range(self.batch_size):
            try:
                dat, lab = self.read_next()
            except IndexError:
                if self.keep_last_batch:
                    break
                else:
                    self.data.seek(0)
                    self.labels.seek(0)
                    raise StopIteration
            data.append(dat)
            labels.append(lab)

        if len(data) == 0:
            self.data.seek(0)
            self.labels.seek(0)
            raise StopIteration

        data = np.stack(data, axis=0)
        labels = np.stack(labels, axis=0)
        # return data, labels
        return mx.nd.array(data), mx.nd.array(labels)

    def read_next(self):
        """
        Read next record from the dataset

        Returns
        -------
        ndarray
            Data record
        int
            Label
        """
        labelline = self.labels.readline()
        if labelline == "":
            raise IndexError
        label = int(labelline)
        data = np.fromstring(self.data.readline(),
                             dtype=self.properties["dtype"],
                             sep=";").reshape(self.properties["data_element_shape"])

        return data, label



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
