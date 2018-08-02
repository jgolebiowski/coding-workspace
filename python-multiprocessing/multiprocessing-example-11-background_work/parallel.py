import math
import multiprocessing
import sys
from datetime import datetime


def worker(rank, size, task_queue=None, result_queue=None):
    while (not task_queue.empty()):
        task = task_queue.get()
        res = cube(task)
        result_queue.put(res)
    print("Finished all tasks on proc {} out of {}".format(rank, size))


class TestWorker(object):
    def __init__(self, list2process, function):
        context = multiprocessing.get_context("spawn")
        max_threads = int(context.cpu_count() / 2) or 1
        self.num_tasks = len(list2process)

        self.task_queue = context.Queue()
        self.result_queue = context.Queue()
        list2process = list2process

        for task in list2process:
            self.task_queue.put(task)

        self.proc = []
        for idx in range(max_threads):
            p = context.Process(target=worker,
                                args=(idx, max_threads),
                                kwargs=dict(task_queue=self.task_queue,
                                            result_queue=self.result_queue
                                            ))
            p.start()
            self.proc.append(p)

        results = []



    def __del__(self):
        for p in self.proc:
            p.terminate()

    def get_results(self):
        results = []
        for elm in range(self.num_tasks):
            results.append(
                (elm, self.result_queue.get())
            )
        return results


class TestIterator(object):
    def __init__(self, list2process):
        self.list2process = list2process

    def __iter__(self):
        print("Iteration p1")
        testworker = TestWorker(self.list2process, cube)
        print("Iteration p2")
        results = testworker.get_results()
        print("Iteration p3")
        for elm in results:
            yield elm





def power(x, power):
    return x ** power


def cube(x):
    return x ** 3


def main():
    list2process = [idx for idx in range(10)]
    for idx in range(100):
        iter = TestIterator(list2process)
        for elm in iter:
            print(elm)


if (__name__ == "__main__"):
    main()
