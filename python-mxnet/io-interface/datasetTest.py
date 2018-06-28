import numpy as np
import shutil
from dataset_libsvm_sparse import write_partition_multiple, DatasetLoader
import unittest
TEST_DATASET = "test_dataset"

class TestDataset(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        # shutil.rmtree(TEST_DATASET, ignore_errors=True)
        pass

    def build_dataset(self, elements, partition_size, dtype=np.float32):
        dataset = [np.random.uniform(0, 1, (2, 2)).astype(dtype) for item in range(elements)]
        labels = [item for item in range(elements)]

        shutil.rmtree(TEST_DATASET, ignore_errors=True)
        write_partition_multiple(dataset, labels, partition_size, TEST_DATASET)
        return dataset, labels

    def run_with_different_args(self, n, b, ps, keep_last_batch=True, partitions_list=None):
        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=partitions_list,
                                   shuffle_partitions=False)
        for idx, (data, labels) in enumerate(dataloader):
            data = data.asnumpy()
            labels = labels.asnumpy()
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
        plist = ['partition-0.libsvm', 'partition-5.libsvm', 'partition-10.libsvm']
        self.run_with_different_args(12, 2, 5, keep_last_batch=False, partitions_list=plist)

    def test_dont_keep(self):
        n = 13
        b = 5
        ps = 3
        plist = ["partition-0.libsvm", "partition-3.libsvm", "partition-6.libsvm", "partition-9.libsvm", "partition-12.libsvm"]

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=False,
                                   partitions_list=plist,
                                   shuffle_partitions=False)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader):
            data = data.asnumpy()
            labels = labels.asnumpy()
            original_data = np.array(dataset[idx * b: (idx + 1) * b])
            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 2)

    def test_single_partition(self):
        self.run_with_different_args(17, 2, 20)

    def test_single_batch(self):
        plist = ['partition-0.libsvm', 'partition-5.libsvm', 'partition-10.libsvm']
        self.run_with_different_args(14, 1, 5, partitions_list=plist)

    def test_iterate_test(self):
        n = 13
        b = 2

        ps = 5
        plist = ['partition-0.libsvm', 'partition-5.libsvm', 'partition-10.libsvm']

        num_examples = 5
        itertions = 3

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=plist,
                                   shuffle_partitions=False)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_test(num_examples, itertions)):
            data = data.asnumpy()
            labels = labels.asnumpy()
            index = idx % 3
            original_data = np.array(dataset[index * b: min((index + 1) * b, num_examples)])

            # print(index * b, min((index + 1) * b, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 9)

    def test_iterate_test_small(self):
        n = 13
        b = 2

        ps = 6
        plist = ['partition-0.libsvm', 'partition-6.libsvm', 'partition-12.libsvm']

        num_examples = 5
        itertions = 3

        dataset, labels = self.build_dataset(n, ps)
        dataloader = DatasetLoader(TEST_DATASET,
                                   batch_size=b,
                                   keep_last_batch=True,
                                   partitions_list=plist,
                                   shuffle_partitions=False)
        n_iterations = 0
        for idx, (data, labels) in enumerate(dataloader.iterate_test(num_examples, itertions)):
            data = data.asnumpy()
            labels = labels.asnumpy()
            index = idx % 3
            original_data = np.array(dataset[index * b: (index + 1) * b])

            # print(index * b, min((index + 1) * b, num_examples))
            # print(idx, data.shape, original_data.shape)

            self.assertTrue(np.allclose(data, original_data))
            n_iterations += 1

        self.assertEqual(n_iterations, 9)


if (__name__ == "__main__"):
    unittest.main()
