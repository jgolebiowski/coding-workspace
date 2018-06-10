from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import multiprocessing as mp
import math
import mp_worker as mpw


def chunks(l, n):
    """Iterator to divide a list into chunks of size n

    Parameters
    ----------
    l : iterable
        list
    n : int
        Chunk size
    """
    n = max(1, n)
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def batchify(l, n):
    """
    Iterator to divide a list into n chunks,
    All but the last are equal size

    Parameters
    ----------
    l : iterable
        list
    n : int
        Number of chunks
    """
    n = min(len(l), n)
    n = max(1, n)
    chunksize = int(math.ceil(len(l) / n))

    for i in range(0, len(l), chunksize):
        # Create an index range for l of chunksize items:
        yield l[i:i + chunksize]


def fast_process_parallel(list2process):
    num_threads = 3

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=mpw.worker_cube,
                       args=(rank, num_threads),
                       kwargs=dict(numbers=batch,
                                   output_queue=output_queue)
                       )
        processes.append(p)

    # Run processes
    for p in processes:
        p.start()

    # Exit completed processes
    for p in processes:
        p.join()

    # Extract results
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())
    print(results)


def main_pool():
    list2process = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    num_threads = 3

    # Create a pool of workers
    globalPool = mp.Pool(processes=num_threads)

    # Start the Queue, this could be also a list, dict etc.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    # Setup a list of processes that we want to run
    for rank in range(len(list2process)):
        # Apply the function asyncronously

        globalPool.apply_async(func=mpw.worker_square_queue,
                               args=(rank, num_threads,),
                               kwds=dict(number=list2process[rank],
                                         output_queue=output_queue)
                               )

    # Do not allow any more entries
    globalPool.close()
    # Join the processes
    globalPool.join()

    # Extract results
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())
    print(results)


def main_process():
    list2process = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    max_num_threads = 5

    # Start the Queue, this could be also a list, dict etc.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    for mini_list in chunks(list2process, max_num_threads):
        num_threads = len(mini_list)
        # Setup a list of processes that we want to run
        processes = []
        for rank in range(num_threads):
            p = mp.Process(target=mpw.worker_square_queue,
                           args=(rank, num_threads),
                           kwargs=dict(number=mini_list[rank],
                                       output_queue=output_queue)
                           )
            processes.append(p)

        # Run processes
        for p in processes:
            p.start()

        # Exit completed processes
        for p in processes:
            p.join()

    # Extract results
    results = []
    while (not output_queue.empty()):
        results.append(output_queue.get())
    print(results)


if (__name__ == "__main__"):
    main_pool()
    main_process()
