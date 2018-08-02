import functools
import multiprocessing
import queue
import time
import numpy as np



def worker(rank, size, tasks_queue=None, results_queue=None):
    while (True):
        try:
            task = tasks_queue.get(block=True, timeout=0.1)
            res = task + 1
            results_queue.put((task, res))
        except queue.Empty:
            print("Finished all tasks on proc {} out of {}".format(rank, size))
            break


class ParallelControl(object):
    def __init__(self, list2process: list):
        context = multiprocessing.get_context("spawn")
        max_threads = max(1, int(context.cpu_count() / 2))

        task_queue = context.Queue()
        result_queue = context.Queue()
        list2process = list2process

        for task in list2process:
            task_queue.put(task)

        proc = []
        for idx in range(max_threads):
            p = context.Process(target=worker,
                                args=(idx, max_threads),
                                kwargs=dict(tasks_queue=task_queue,
                                            results_queue=result_queue
                                            ))
            p.start()
            proc.append(p)

        self.result_queue = result_queue
        self.task_queue = task_queue
        self.num_tasks = len(list2process)
        self.proc = proc

    def get_results(self):
        results = []
        for idx in range(self.num_tasks):
            results.append(self.result_queue.get())

        return results

    def __del__(self):
        self.task_queue.close()
        self.result_queue.close()
        for p in self.proc:
            p.join()
            p.terminate()


if __name__ == '__main__':
    pc = ParallelControl([np.random.uniform(0, 1, (100, 100)) for idx in range(10)])
    res = pc.get_results()
    # print(res)

    # This is here so that the __del__ method wont be called before the thread starts
    time.sleep(0.1)
