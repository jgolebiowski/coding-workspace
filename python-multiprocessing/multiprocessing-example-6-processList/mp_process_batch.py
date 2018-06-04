from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import multiprocessing as mp
from mp_worker import worker_square, worker_square_list


def chunks(l, n):
    """Iterator to divide a list into chunks of size n

    Parameters
    ----------
    l : iterable
        list
    n : int
        Chunk size
    """
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def main():
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
            p = mp.Process(target=worker_square_list,
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
        while(not output_queue.empty()):
            results.append(output_queue.get())
        print(results)


if (__name__ == "__main__"):
    main()
