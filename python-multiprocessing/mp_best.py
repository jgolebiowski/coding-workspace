import multiprocessing as mp
import math


def cube(x):
    return x ** 3


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


def paralll_worker(rank, size,
                   batch=None,
                   output_queue=None):
    """
    Function to perform parallel work on a function and dump the results
    into the output queue, each entry will be structured as
    (rank, function_input, function_output)
    Parameters
    ----------
    rank : int
        process number
    size : int
        total number of processes
    batch : list[object]
        Inputs to the function
    output_queue : mp.Queue
        Quete to store the results in
    """
    print("This is process {} out of {} operating on {}".format(rank, size, batch))
    for input in batch:
        result = cube(input)
        output_queue.put((rank, input, result))


def parallel_control(list2process, num_threads):
    """Process a list in parallel by spawning only necessary number of processes
    Parameters
    ----------
    list2process : list
        List with inputs to process
    num_threads : int
        Number of threads ot use
    """

    # Start the Queue, this could be also a list, dict or a shared array.
    mp_manager = mp.Manager()
    output_queue = mp_manager.Queue()

    processes = []
    for rank, batch in enumerate(batchify(list2process, num_threads)):
        p = mp.Process(target=paralll_worker,
                       args=(rank, num_threads),
                       kwargs=dict(batch=batch,
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

    return results


def main():
    list2process = list(range(10))
    print(parallel_control(list2process, 3))


if (__name__ == "__main__"):
    main()