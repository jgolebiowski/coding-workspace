import numpy as np
import os
import time
from dataset_mxnet import MXRecordGenerator, MXRecordLoader
from dataset_hdf5 import HDF5Generator, HDF5Loader
from dataset_libsvm import write_partition_multiple, DatasetLoader
DTYPE=np.float32

def main():
    dataset_path = os.path.join("data", "partition")
    new_dataset_path = os.path.join("data", "dataset")
    n = 50000
    batch = 16
    dataset = [np.random.uniform(0, 1, (1, 28, 28)).astype(DTYPE) for item in range(n)]
    labels = [item for item in range(n)]

    begin = time.time()
    gen = MXRecordGenerator(dataset_path)
    for dat, lab in zip(dataset, labels):
        gen.write(dat, lab)
    gen.record.close()
    print("MXnet write", time.time() - begin)

    begin = time.time()
    loader = MXRecordLoader(dataset_path, batch_size=batch)
    for idx, (data, label) in enumerate(loader):
        # print(idx, data)
        data[0, 0] += 1
        pass
    print("MXnet read", time.time() - begin)

    begin = time.time()
    gen = HDF5Generator(dataset_path)
    gen.initialize_from_data(dataset, labels)
    gen.hdf5.close()
    print("HDF5 write", time.time() - begin)

    begin = time.time()
    loader = HDF5Loader(dataset_path, batch_size=batch)
    for idx, (data, label) in enumerate(loader):
        # print(idx, data.shape)
        data[0, 0] += 1
        pass
    print("HDF5 read", time.time() - begin)

    begin = time.time()
    write_partition_multiple(dataset, labels, 1000, new_dataset_path)
    print("Dataset write", time.time() - begin)

    begin = time.time()
    dataloader = DatasetLoader(new_dataset_path, batch_size=batch)
    for idx, (data, labels) in enumerate(dataloader):
        # print(idx, data.shape)
        data[0, 0] += 1
        pass
    print("Dataset read", time.time() - begin)

if (__name__ == "__main__"):
    main()
