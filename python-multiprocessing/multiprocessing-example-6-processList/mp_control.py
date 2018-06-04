from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import multiprocessing as mp
from mp_worker import worker_square, worker_square_list, worker_square_queue


def main_pool():
    num_threads = 3

    # Create a pool of workers
    globalPool = mp.Pool(processes=num_threads)
    resultsQueue = []

    # Setup a list of processes that we want to run
    for rank in range(num_threads):
        # Apply the function asyncronously

        localResult = globalPool.apply_async(worker_square,
                                             (rank, num_threads),
                                             dict(number=rank))
        resultsQueue.append(localResult)

    # Do not allow any more entries
    globalPool.close()
    # Join the processes
    globalPool.join()

    # Get results from the queueu
    results = [item.get() for item in resultsQueue]
    print(results)


def main_queue():
    num_threads = 3

    # Start the Queue, this could be also a list, dict etc.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    # Setup a list of processes that we want to run
    processes = []
    for rank in range(num_threads):
        p = mp.Process(target=worker_square_queue,
                       args=(rank, num_threads),
                       kwargs=dict(number=rank,
                                   output_queue=output_queue)
                       )
        processes.append(p)

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Extract results
    results = [None for i in range(num_threads)]
    for rank in range(num_threads):
        res = output_queue.get()
        results[res[0]] = res[2]
    print(results)


def main_list():
    num_threads = 3

    # Start the list, this could be also a list, dict etc.
    mp_manager = mp.Manager()
    output_list = mp_manager.list([None for i in range(num_threads)])

    # Setup a list of processes that we want to run
    processes = []
    for rank in range(num_threads):
        p = mp.Process(target=worker_square_list,
                       args=(rank, num_threads),
                       kwargs=dict(number=rank,
                                   output_list=output_list)
                       )
        processes.append(p)

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    print(output_list)


if (__name__ == "__main__"):
    main_pool()
    main_queue()
    main_list()
