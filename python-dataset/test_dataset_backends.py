import os
import shutil
import unittest

import numpy as np

from dataset_backends import libsvm_load_partition, libsvm_write_partition, libsvm_load_partition_sparse_parallel
from dataset_backends import numpy_load_partition, numpy_write_partition

PARTITION_PREFIX = ""
TEST_DATASET = "test_dataset"


class TestDataset(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)

    @classmethod
    def setUpClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)

    def run_test_dataset(self, elements, dtype=np.float32, writer=None, loader=None, partition_suffix=""):
        dataset = [np.random.uniform(0, 1, (3, 3, 3, 3)).astype(dtype) for item in range(elements)]
        labels = [item for item in range(elements)]

        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        os.mkdir(TEST_DATASET)
        writer(dataset,
               labels,
               "testpartition" + partition_suffix,
               TEST_DATASET)

        dat, lab = loader("testpartition" + partition_suffix, TEST_DATASET)

        self.assertTrue(np.allclose(dat, dataset))
        self.assertTrue(np.allclose(lab, labels))

    def run_libsvm_parallel(self, elements, dtype=np.float32, writer=None, loader=None, partition_suffix=""):
        dataset = [np.random.uniform(0, 1, (3, 3, 3, 3)).astype(dtype) for item in range(elements)]
        labels = [item for item in range(elements)]

        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        os.mkdir(TEST_DATASET)
        writer(dataset[0: int(elements / 2)],
               labels[0: int(elements / 2)],
               "testpartition" + partition_suffix,
               TEST_DATASET)
        writer(dataset[int(elements / 2):],
               labels[int(elements / 2):],
               "testpartition2" + partition_suffix,
               TEST_DATASET)

        dat, datashape, lab = libsvm_load_partition_sparse_parallel(
            ["testpartition" + partition_suffix, "testpartition2" + partition_suffix],
            TEST_DATASET)

        dat = dat.toarray()
        dat = dat.reshape((-1,) + datashape)
        self.assertTrue(np.allclose(dat, dataset))
        self.assertTrue(np.allclose(lab, labels))

    def test_libsvm_dense(self):
        for elm in [3, 7, 100]:
            self.run_test_dataset(elm, writer=libsvm_write_partition, loader=libsvm_load_partition, partition_suffix="")

    def test_libsvm_parallel(self):
        for elm in [3, 7, 100]:
            self.run_libsvm_parallel(elm, writer=libsvm_write_partition, loader=libsvm_load_partition,
                                     partition_suffix="")

    def test_numpy(self):
        for elm in [3, 7, 100]:
            self.run_test_dataset(elm, writer=numpy_write_partition, loader=numpy_load_partition,
                                  partition_suffix=".npz")


if (__name__ == "__main__"):
    unittest.main()
