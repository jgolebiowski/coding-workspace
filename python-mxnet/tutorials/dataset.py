"""This is my own implementation of the dataset"""
from mxnet.gluon.data import Dataset
from mxnet import ndarray

class ListDataset(Dataset):
    """A dataset that combines multiple dataset-like objects, e.g.
    Datasets, lists, arrays, etc.

    The i-th sample is defined as `(x1[i], x2[i], ...)`.

    Parameters
    ----------
    *args : one or more dataset-like objects
        The data arrays.
    """
    def __init__(self, *args):
        assert len(args) > 0, "Needs at least 1 arrays"
        self._length = len(args[0])
        self._data = []
        for i, data in enumerate(args):
            assert len(data) == self._length, \
                "All arrays must have the same length; array[0] has length %d " \
                "while array[%d] has %d." % (self._length, i+1, len(data))
            if isinstance(data, ndarray.NDArray) and len(data.shape) == 1:
                data = data.asnumpy()
            self._data.append(data)

    def __getitem__(self, idx):
        if len(self._data) == 1:
            return self._data[0][idx]
        else:
            return tuple(data[idx] for data in self._data)

    def __len__(self):
        return self._length