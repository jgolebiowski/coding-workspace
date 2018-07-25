import numpy as np
import shutil
from dataset import DatasetLoader
from dataset_backends import write_partition_multiple, numpy_load_partition, numpy_write_partition

import unittest

TEST_DATASET = "test_dataset"
PARTITION_SUFFIX = ".npz"


class TestDataset(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        pass

    def build_dataset(self, elements, partition_size, dtype=np.float32):
        dataset = [np.random.uniform(0, 1, (2, 2)).astype(dtype) for item in range(elements)]
        labels = [item for item in range(elements)]

        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        write_partition_multiple(dataset, labels, partition_size, TEST_DATASET, writer=numpy_write_partition)
        return dataset, labels

    def run_with_different_args(self, n, b, ps, keep_last_batch=True, partitions_list=None):
        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=partitions_list,
                                   shuffle_partitions=False,
                                   partition_loder=numpy_load_partition)
        for idx, (data, labels) in enumerate(dataloader):
            original_data = np.array(dataset[idx * b: (idx + 1) * b])
            self.assertTrue(np.allclose(data, original_data))

    def test_settings(self):
        """Test basinc setup"""
        self.run_with_different_args(10, 5, 5)
        self.run_with_different_args(10, 1, 3)
        self.run_with_different_args(11, 5, 3)

    @unittest.expectedFailure
    def test_wrong_list(self):
        self.run_with_different_args(20, 5, 5)

    def test_carry_over(self):
        plist = ['partition-0' + PARTITION_SUFFIX, 'partition-5' + PARTITION_SUFFIX, 'partition-10' + PARTITION_SUFFIX]
        self.run_with_different_args(12, 2, 5, keep_last_batch=False, partitions_list=plist)

    def test_dont_keep(self):
        n = 13
        b = 5
        ps = 3
        plist = ["partition-0" + PARTITION_SUFFIX, "partition-3" + PARTITION_SUFFIX, "partition-6" + PARTITION_SUFFIX,
                 "partition-9" + PARTITION_SUFFIX, "partition-12" + PARTITION_SUFFIX]

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=False,
                                   partitions_list=plist,
                                   shuffle_partitions=False,
                                   partition_loder=numpy_load_partition)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader):
            data = data
            labels = labels
            original_data = np.array(dataset[idx * b: (idx + 1) * b])
            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 2)

    def test_single_partition(self):
        self.run_with_different_args(17, 2, 20)

    def test_single_batch(self):
        plist = ['partition-0' + PARTITION_SUFFIX, 'partition-5' + PARTITION_SUFFIX, 'partition-10' + PARTITION_SUFFIX]
        self.run_with_different_args(14, 1, 5, partitions_list=plist)

    def test_iterate_single_partition(self):
        n = 13
        b = 2

        ps = 5
        plist = ['partition-0' + PARTITION_SUFFIX, 'partition-5' + PARTITION_SUFFIX, 'partition-10' + PARTITION_SUFFIX]

        num_examples = 5
        itertions = 3

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=plist,
                                   shuffle_partitions=False,
                                   partition_loder=numpy_load_partition)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_single_partition(num_examples, itertions)):
            data = data
            labels = labels
            index = idx % 3
            original_data = np.array(dataset[index * b: min((index + 1) * b, num_examples)])

            # print(index * b, min((index + 1) * b, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 9)

    def test_iterate_single_partition2(self):
        n = 13
        b = 2

        ps = 5

        num_examples = -1
        itertions = 3

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=False,
                                   shuffle_partitions=False,
                                   partition_loder=numpy_load_partition)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_single_partition(num_examples,
                                                                                 itertions,
                                                                                 partition_name='partition-0' + PARTITION_SUFFIX)):
            data = data
            labels = labels
            index = idx % 2
            original_data = np.array(dataset[index * b: (index + 1) * b])

            # print(index * b, min((index + 1) * b, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 6)

    def test_iterate_single_partition3(self):
        n = 13
        b = 2

        ps = 6
        plist = ['partition-0' + PARTITION_SUFFIX, 'partition-6' + PARTITION_SUFFIX, 'partition-12' + PARTITION_SUFFIX]

        num_examples = 5
        itertions = 3

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=plist,
                                   shuffle_partitions=False,
                                   partition_loder=numpy_load_partition)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_single_partition(num_examples, itertions)):
            data = data
            labels = labels
            index = idx % 3
            original_data = np.array(dataset[index * b: (index + 1) * b])

            # print(index * b, min((index + 1) * b, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 9)


if (__name__ == "__main__"):
    unittest.main()
