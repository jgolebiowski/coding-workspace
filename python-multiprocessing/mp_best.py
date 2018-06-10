import multiprocessing as mp
import math


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


def worker_cube(rank, size,
                output_queue=None,
                numbers=None):
    """
    Function to calcuate the cube of a numbers in a givne list.
    For each number, put
    tuple (int, float, float)
        (rank, number, number_squared)
    Into the Queue

    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    output_queue : mp.Queue
        Quete to store the results in
    number : list[float]
        Numbers to cube
    """
    print("This is process {} out of {} operating on {}".format(rank, size, numbers))
    for number in numbers:
        output_queue.put((rank, number, number ** 3))


def fast_process_parallel(list2process, num_threads):
    """Process a list in parallel by spawning only necessary number of processes"""

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=worker_cube,
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


def main():
    list2process = list(range(10))
    fast_process_parallel(list2process, 3)


if (__name__ == "__main__"):
    main()
