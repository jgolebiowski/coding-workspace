import shutil
import unittest

import numpy as np

from dataset import DatasetLoaderFactory
from dataset_backends import libsvm_write_partition
from dataset_backends import numpy_write_partition
from dataset_backends import write_partition_multiple
TEST_DATASET = "test_dataset"

class TestDataset(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)

    @classmethod
    def setUpClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)

    def build_dataset(self, elements, partition_size, ploader):
        dtype = np.float32
        dataset = [np.random.uniform(0, 1, (2, 2)).astype(dtype) for item in range(elements)]
        labels = [item for item in range(elements)]

        if "numpy" in ploader:
            writer = numpy_write_partition
        elif "libsvm" in ploader:
            writer = libsvm_write_partition
        else:
            raise ValueError("Wrong partition loader specified")

        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        write_partition_multiple(dataset, labels, partition_size, TEST_DATASET, writer=writer)
        return dataset, labels

    def run_test(self, nelements, batchsize, partitionsize, ploader, keep_last_batch, shuffle, memory):
        dataset, labels_set = self.build_dataset(nelements, partitionsize, ploader)
        dataloader = DatasetLoaderFactory(TEST_DATASET,
                                          partition_loader=ploader,
                                          batch_size=batchsize,
                                          keep_last_batch=keep_last_batch,
                                          shuffle_partitions=shuffle,
                                          save_in_memory=memory)

        for idx, (data, labels) in enumerate(dataloader):
            data = data
            labels = labels
            original_data = np.array(dataset[idx * batchsize: (idx + 1) * batchsize])
            original_labels = np.array(labels_set[idx * batchsize: (idx + 1) * batchsize])
            self.assertTrue(np.allclose(data, original_data))
            self.assertTrue(np.allclose(labels, original_labels))

    def run_test_shuffle(self, nelements, batchsize, partitionsize, ploader, keep_last_batch, shuffle, memory):
        dataset, labels_set = self.build_dataset(nelements, partitionsize, ploader)
        dataloader = DatasetLoaderFactory(TEST_DATASET,
                                          partition_loader=ploader,
                                          batch_size=batchsize,
                                          keep_last_batch=keep_last_batch,
                                          shuffle_partitions=shuffle,
                                          save_in_memory=memory)

        indexes = []
        for idx, (data, labels) in enumerate(dataloader):
            indexes.append(idx)

        for idx, (data, labels) in enumerate(dataloader):
            data = data
            labels = labels
            self.assertTrue(
                any(
                    [np.allclose(data, np.array(dataset[i * batchsize: (i + 1) * batchsize])) for i in indexes]
                ))
            self.assertTrue(
                any(
                    [np.allclose(labels, np.array(labels_set[i * batchsize: (i + 1) * batchsize])) for i in indexes]
                ))

    def run_test_dont_keep(self, ploader, memory):
        nelements = 13
        batchsize = 5
        partitionsize = 3

        dataset, labels_set = self.build_dataset(nelements, partitionsize, ploader)
        dataloader = DatasetLoaderFactory(TEST_DATASET,
                                          partition_loader=ploader,
                                          batch_size=batchsize,
                                          keep_last_batch=False,
                                          shuffle_partitions=False,
                                          save_in_memory=memory)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader):
            data = data
            labels = labels
            original_data = np.array(dataset[idx * batchsize: (idx + 1) * batchsize])
            original_labels = np.array(labels_set[idx * batchsize: (idx + 1) * batchsize])
            self.assertTrue(np.allclose(data, original_data))
            self.assertTrue(np.allclose(labels, original_labels))
            n_iterations += 1

        self.assertEqual(n_iterations, 2)

    def run_test_iterate_single_partition(self, ploader, memory):
        nelements = 13
        batchsize = 2
        partitionsize = 6
        dataset, labels_set = self.build_dataset(nelements, partitionsize, ploader)
        dataloader = DatasetLoaderFactory(TEST_DATASET,
                                          partition_loader=ploader,
                                          batch_size=batchsize,
                                          keep_last_batch=False,
                                          shuffle_partitions=False,
                                          save_in_memory=memory,
                                          max_threads=1)

        num_examples = partitionsize
        itertions = 3

        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_single_partition(num_examples, itertions)):
            data = data
            labels = labels
            index = idx % 3
            original_data = np.array(dataset[index * batchsize: min((index + 1) * batchsize, num_examples)])
            original_labels = np.array(labels_set[index * batchsize: min((index + 1) * batchsize, num_examples)])

            # print(index * batchsize, min((index + 1) * batchsize, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            self.assertTrue(np.allclose(original_labels, labels))
            n_iterations += 1

        self.assertEqual(n_iterations, 9)

    def test_settings(self):
        for ploader in ["numpy", "libsvm-dense", "libsvm-sparse", "libsvm-sparse-parallel"]:
            for memory in [True, False]:
                self.run_test_dont_keep(ploader, memory)
                self.run_test_iterate_single_partition(ploader, memory)
                for nelements, batchsize, partitionsize in [(9, 1, 3), (12, 2, 4), (15, 1, 5)]:
                    self.run_test_shuffle(nelements, batchsize, partitionsize, ploader, False, True, memory)

                for nelements in [4, 9, 15]:
                    for batchsize in [1, 3, 5]:
                        for partitionsize in [2, 3, 5]:
                            for keep in [True, False]:
                                self.run_test(nelements, batchsize, partitionsize, ploader, keep, False, memory)



if (__name__ == "__main__"):
    unittest.main()
