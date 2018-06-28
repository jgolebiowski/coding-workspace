import mxnet as mx
import numpy as np

DATATYPE = np.float32

class MXRecordGenerator(object):
    """
    Generate a MXRecordIO Dataset by appending examples one by one

    Parameters
    ----------
    filepath : str
        Path to the dataset record file

    """

    def __init__(self, filepath):
        if filepath.endswith(".rec"):
            self.record = mx.recordio.MXRecordIO(filepath, 'w')
        else:
            self.record = mx.recordio.MXRecordIO(filepath + ".rec", 'w')

        self.dtype = DATATYPE
        self.id2 = 0

    def __del__(self):
        self.record.close()

    def write(self, data, label, id=0):
        """
        Write a new record to the dataset

        Parameters
        ----------
        data : ndarray
            Data to be stored, should be in "C" order (Row Major) and in the
            dtype specified in self.dtype
        label : int
            The label for this data
        id : int
            Id of this entry

        """
        if data.dtype != self.dtype:
            raise ValueError("Wrong datatype {} != {}".format(data.dtype, self.dtype))
        header = mx.recordio.IRHeader(flag=0, label=data.shape, id=id, id2=label)
        packed = mx.recordio.pack(header, data.tobytes("C"))
        self.record.write(packed)
        self.id2 += 1


class MXRecordLoader(object):
    """
    A dataset utility for loading contents of a RecordIO (.rec) file written by MXRecordGenerator.

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
        if filepath.endswith(".rec"):
            self.record = mx.recordio.MXRecordIO(filepath, 'r')
        else:
            self.record = mx.recordio.MXRecordIO(filepath + ".rec", 'r')

        self.batch_size = batch_size
        self.keep_last_batch = keep_last_batch
        self.dtype = DATATYPE

    def __del__(self):
        self.record.close()

    def __iter__(self):
        self.record.reset()
        return self

    def __next__(self):
        # results = [self.nextitem() for item in range(self.batch_size)]
        # data, labels = zip(*results)

        data = []
        labels = []
        for idx in range(self.batch_size):
            try:
                dat, lab = self.nextitem()
            except IndexError:
                if self.keep_last_batch:
                    break
                else:
                    raise StopIteration
            data.append(dat)
            labels.append(lab)

        if len(data) == 0:
            raise StopIteration

        data = np.stack(data, axis=0)
        labels = np.stack(labels, axis=0)
        return mx.nd.array(data), mx.nd.array(labels)


    def nextitem(self):
        """
        Read next record from the dataset

        Returns
        -------
        ndarray
            Next data record, None if the whole dataset is read
        int
            Label, None if the whole dataset is read
        """
        packed = self.record.read()
        if packed is None:
            raise IndexError
        unpacked = mx.recordio.unpack(packed)
        header = unpacked[0]
        shape = [int(item) for item in header.label]
        label = unpacked[0].id2

        data = np.frombuffer(unpacked[1], dtype=self.dtype).reshape(shape)
        return data, label

