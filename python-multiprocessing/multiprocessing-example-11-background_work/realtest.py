import multiprocessing
import queue

import scipy.sparse
import numpy as np


def worker(rank, size, task_queue=None, result_queue=None):
    while (True):
        try:
            task = task_queue.get_nowait()
            res = task + "processed"
            result_queue.put(res)
        except queue.Empty:
            print("Finished all tasks on proc {} out of {}".format(rank, size))
            break


class AsyncParallelreader(object):
    def __init__(self, list2process):
        print("Initializing the reader")
        context = multiprocessing.get_context("spawn")
        print("Initializing the reader2")
        max_threads = int(context.cpu_count() / 2)
        print("Initializing the reader3")
        self.num_tasks = len(list2process)
        print("Initializing the reader4")

        self.task_queue = context.Queue()
        self.result_queue = context.Queue()
        print("Initializing the reader5")
        list2process = list2process

        print("Initializing the reader6")
        for task in list2process:
            self.task_queue.put(task)

        print("Initializing the reader7")
        self.proc = []
        for idx in range(max_threads):
            print("Initializing the reader8")
            p = context.Process(target=worker,
                                args=(idx, max_threads),
                                kwargs=dict(task_queue=self.task_queue,
                                            result_queue=self.result_queue
                                            ))
            print("Initializing the reader9")
            p.start()
            self.proc.append(p)
        print("Initializing the reader10")


    def __del__(self):
        self.task_queue.close()
        self.result_queue.close()
        for p in self.proc:
            p.join()
            p.terminate()

    def get_results(self):
        return self.result_queue.get()




class SparseDatasetLoaderParquetParallel(object):
    partitions_list = ["1", "2"]
    batch_size = 16
    sparse=True


    def __init__(self, *args, max_queue_size=30, max_threads=None):
        super().__init__()
        self.max_queue_size = max_queue_size
        if max_threads is None:
            max_threads = max(1, int(multiprocessing.cpu_count() / 2))
        self.max_threads = max_threads

    def __iter__(self):
        print("Starting iteration", self.partitions_list)
        apr = AsyncParallelreader(self.partitions_list)

        print("Initialized new apr")
        for pidx, partition in enumerate(self.partitions_list):
            print("Iteration {}, result: {}".format(pidx, apr.get_results()))

            # data, datashape, extra_features, labels = dataframe2data(parquet_load_partition(partition, self.dataset_path))
            data = scipy.sparse.csr_matrix((100, 1000), dtype="float32")
            datashape = (10, 10, 10)
            extra_features = np.random.uniform(0, 1, (100, 2))
            labels = np.random.uniform(0, 1, (100))
            partition_length = len(labels)
            starting_index = 0
            for idx in range(starting_index, partition_length, self.batch_size):
                print("loading {} batch of {}p".format(idx, pidx))
                dat = data[idx: min(idx + self.batch_size, partition_length)]
                extra = extra_features[idx: min(idx + self.batch_size, partition_length)]
                lab = labels[idx: min(idx + self.batch_size, partition_length)]
                yield (dat, datashape, extra), lab



def run_test():
    train_dataloader = SparseDatasetLoaderParquetParallel(1, 2, 3)
    for e in range(4):
        for idx, (batch_data, label) in enumerate(train_dataloader):
            print(e, idx)

if __name__ == '__main__':
    run_test()